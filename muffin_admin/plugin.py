"""Setup the plugin."""

import typing as t
from inspect import isclass
from pathlib import Path

from asgi_tools.utils import to_awaitable
from muffin import Application, ResponseFile, ResponseRedirect, ResponseError, Request
from muffin.plugins import BasePlugin
from muffin_rest.api import API, AUTH

from .handler import AdminHandler


PACKAGE_DIR: Path = Path(__file__).parent
TEMPLATE: str = (PACKAGE_DIR / 'admin.html').read_text()


async def page404(request: Request) -> ResponseError:
    """Default 404 for authorization methods."""
    return ResponseError.NOT_FOUND()


class Plugin(BasePlugin):

    """Admin interface for Muffin Framework."""

    name = 'admin'
    defaults = {
        'prefix': '/admin',
        'title': 'Muffin Admin',

        'custom_js_url': '',
        'custom_css_url': '',

        'login_url': None,
        'logout_url': None,

        'auth_storage': 'localstorage',  # localstorage|cookies
        'auth_storage_name': 'muffin_admin_auth',
        'app_bar_links': [
            {'url': '/', 'icon': 'Home', 'title': 'Home'},
        ],
    }

    def __init__(self, *args, **kwargs):
        self.api: API = API()
        self.auth: t.Dict = {}
        self.handlers: t.List = []
        self.__login__ = self.__ident__ = page404
        self.__dashboard__ = None
        super(Plugin, self).__init__(*args, **kwargs)

    def setup(self, app: Application, **options):
        """Initialize the application."""
        super().setup(app, **options)
        self.api.setup(app, prefix=f"{self.cfg.prefix}/api", openapi=False)

        self.auth['storage'] = self.cfg.auth_storage
        self.auth['storage_name'] = self.cfg.auth_storage_name
        self.auth['loginURL'] = self.cfg.login_url
        self.auth['logoutURL'] = self.cfg.logout_url

        custom_js = self.cfg.custom_js_url
        custom_css = self.cfg.custom_css_url
        title = self.cfg.title
        prefix = self.cfg.prefix

        def authorize(view):
            """Authorization."""
            async def decorator(request):
                """Authorize an user."""
                if self.api.authorize:
                    auth = await self.api.authorize(request)
                    if not auth:
                        if self.cfg.login_url:
                            return ResponseRedirect(self.cfg.login_url)

                return await view(request)

            return decorator

        @app.route(self.cfg.prefix)
        @authorize
        async def render_admin(request):
            """Render admin page."""
            return TEMPLATE.format(
                prefix=prefix, title=title,
                custom_js=f"<script src={custom_js} />" if custom_js else '',
                custom_css=f"<link rel='stylesheet' href={custom_css} />" if custom_css else '',
            )

        @app.route(f"{self.cfg.prefix}/ra.json")
        @authorize
        async def ra(request):
            data = self.to_ra()

            if self.__dashboard__:
                data['dashboard'] = await self.__dashboard__(request)

            return data

        @app.route(f"{ self.cfg.prefix }/main.js")
        async def render_admin_static(request):
            return ResponseFile(PACKAGE_DIR / 'main.js')

        @app.route(f"{self.cfg.prefix}/login")
        async def login(request):
            return await self.__login__(request)

        @app.route(f"{self.cfg.prefix}/ident")
        async def ident(request):
            return await self.__ident__(request)

    def route(self, path: t.Any, *paths: str, **params) -> t.Callable:
        """Route an handler."""
        if not isinstance(path, str):
            self.register_handler(path)
            return self.api.route(path)

        paths = (path, *paths)

        def wrapper(cb):
            self.register_handler(cb)
            return self.api.route(*paths, **params)(cb)

        return wrapper

    def register_handler(self, handler: t.Any):
        """Register an handler."""
        if isclass(handler) and issubclass(handler, AdminHandler):
            self.handlers.append(handler)

    # Authorization flow
    # ------------------

    def check_auth(self, fn: AUTH) -> AUTH:
        """Register a function to authorize current user."""
        self.auth['required'] = True
        self.api.authorize = fn
        return fn

    def login(self, fn: AUTH) -> AUTH:
        """Register a function to login current user."""
        self.auth['authorizeURL'] = f"{self.cfg.prefix}/login"
        self.__login__ = to_awaitable(fn)
        return fn

    def dashboard(self, fn: AUTH) -> AUTH:
        """Register a function to render dashboard."""
        self.__dashboard__ = to_awaitable(fn)
        return fn

    def get_identity(self, fn: AUTH) -> AUTH:
        """Register a function to identificate current user.

        User data: {id, fullName, avatar}
        """
        self.auth['identityURL'] = f"{ self.cfg.prefix }/ident"
        self.__ident__ = to_awaitable(fn)
        return fn

    # Serialize to react-admin
    # -------------------------

    def to_ra(self) -> t.Dict:
        """Prepare params for react-admin."""
        from . import __version__

        return {
            "apiUrl": f"{self.cfg.prefix}/api",
            "auth": self.auth,
            "adminProps": {
                "title": self.cfg.title,
                "disableTelemetry": True,
            },
            "appBarLinks": self.cfg.app_bar_links,
            "resources": [res.to_ra() for res in self.handlers],
            "version": __version__,
        }
