"""Setup the plugin."""

from inspect import isclass
from pathlib import Path

from asgi_tools._compat import json_dumps
from muffin import Application, ResponseFile, ResponseError, ResponseRedirect
from muffin.plugin import BasePlugin
from muffin_rest.api import API, AUTH

from .handler import AdminHandler


PACKAGE_DIR = Path(__file__).parent
TEMPLATE = (PACKAGE_DIR / 'admin.html').read_text()


async def page404(request):
    """Default 404 for authorization methods."""
    return ResponseError.NOT_FOUND()


class Plugin(BasePlugin):

    """Admin interface for Muffin Framework."""

    name = 'admin'
    defaults = {
        'prefix': '/admin',
        'title': 'Muffin Admin',

        'auth_redirect_url': None,
        'auth_storage': 'localstorage',  # localstorage|cookies
        'auth_storage_name': 'muffin_admin_auth',
    }

    def __init__(self, *args, **kwargs):
        self.api = API()
        self.auth = {}
        self.handlers = []
        self.__login__ = self.__ident__ = page404
        super(Plugin, self).__init__(*args, **kwargs)

    def setup(self, app: Application, **options):
        """Initialize the application."""
        super().setup(app, **options)
        self.api.setup(app, prefix=f"{self.cfg.prefix}/api", openapi=False)

        self.auth['storage'] = self.cfg.auth_storage
        self.auth['storage_name'] = self.cfg.auth_storage_name

        @app.route(self.cfg.prefix)
        async def render_admin(request):
            if self.cfg.auth_redirect_url and self.api.authorize:
                auth = await self.api.authorize(request)
                if not auth:
                    return ResponseRedirect(self.cfg.auth_redirect_url)

            return TEMPLATE.format(admin=self, title=self.app.cfg.name.title())

        @app.route(f"{ self.cfg.prefix }/main.js")
        async def render_admin_static(request):
            return ResponseFile(PACKAGE_DIR / 'main.js')

        @app.route(f"{self.cfg.prefix}/login")
        async def login(request):
            return await self.__login__(request)

        @app.route(f"{self.cfg.prefix}/ident")
        async def ident(request):
            return await self.__ident__(request)

    def route(self, path, *paths, **params):
        """Route an handler."""
        if not isinstance(path, str):
            self.register_handler(path)
            return self.api.route(path)

        paths = (path, *paths)

        def wrapper(cb):
            self.register_handler(cb)
            return self.api.route(*paths, **params)(cb)

        return wrapper

    def register_handler(self, handler):
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
        self.auth['loginURL'] = f"{self.cfg.prefix}/login"
        self.__login__ = fn
        return fn

    def get_identity(self, fn: AUTH) -> AUTH:
        """Register a function to identificate current user."""
        self.auth['identityURL'] = f"{ self.cfg.prefix }/ident"
        self.__ident__ = fn
        return fn

    # Serialize to react-admin
    # -------------------------

    @property
    def json(self):
        """Jsonify the plugin."""
        return json_dumps(self.to_ra()).decode('utf-8')

    def to_ra(self):
        """Prepare params for react-admin."""
        return {
            "apiUrl": f"{self.cfg.prefix}/api",
            "auth": self.auth,
            "adminProps": {
                "title": self.cfg.title,
                "disableTelemetry": True,
            },
            "resources": [res.to_ra() for res in self.handlers],
        }
