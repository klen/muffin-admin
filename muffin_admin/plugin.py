"""Setup the plugin."""

from __future__ import annotations

from importlib import metadata
from inspect import isclass
from pathlib import Path
from typing import Any, Callable, ClassVar, Dict, List, Optional, Type, cast

from muffin import Application, Request, ResponseError, ResponseFile, ResponseRedirect
from muffin.plugins import BasePlugin
from muffin_rest.api import API
from muffin_rest.types import TAuth

from .handler import AdminHandler

PACKAGE_DIR: Path = Path(__file__).parent
TEMPLATE: str = (PACKAGE_DIR / "admin.html").read_text()
VERSION = metadata.version("muffin-admin")


async def page404(_: Request) -> ResponseError:
    """Default 404 for authorization methods."""
    return ResponseError.NOT_FOUND()


class Plugin(BasePlugin):

    """Admin interface for Muffin Framework."""

    name = "admin"
    defaults: ClassVar[Dict[str, Any]] = {
        "prefix": "/admin",
        "title": "Muffin-Admin",
        "main_js_url": "{prefix}/main.js",
        "custom_js_url": "",
        "custom_css_url": "",
        "login_url": None,
        "logout_url": None,
        "menu_sort": True,
        "auth_storage": "localstorage",  # localstorage|cookies
        "auth_storage_name": "muffin_admin_auth",
        "app_bar_links": [
            {"url": "/", "icon": "Home", "title": "Home"},
        ],
        "mutation_mode": "optimistic",
    }

    def __init__(self, app: Optional[Application] = None, **kwargs):
        self.api: API = API()
        self.auth: Dict = {}
        self.handlers: List[Type[AdminHandler]] = []
        self.__login__ = self.__ident__ = cast(TAuth, page404)
        self.__dashboard__: Optional[TAuth] = None
        super(Plugin, self).__init__(app, **kwargs)

    def setup(self, app: Application, **options):  # noqa: C901
        """Initialize the application."""
        super().setup(app, **options)
        self.cfg.update(prefix=self.cfg.prefix.rstrip("/"))
        self.api.setup(app, prefix=f"{self.cfg.prefix}/api", openapi=False)

        self.auth["storage"] = self.cfg.auth_storage
        self.auth["storageName"] = self.cfg.auth_storage_name
        self.auth["loginURL"] = self.cfg.login_url
        self.auth["logoutURL"] = self.cfg.logout_url

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
                    if not auth and self.cfg.login_url:
                        return ResponseRedirect(self.cfg.login_url)

                return await view(request)

            return decorator

        @authorize
        async def render_admin(_):
            """Render admin page."""
            return TEMPLATE.format(
                prefix=prefix,
                title=title,
                main_js_url=self.cfg.main_js_url.format(prefix=prefix),
                custom_js=f"<script src={custom_js}></script>" if custom_js else "",
                custom_css=f"<link rel='stylesheet' href={custom_css} />" if custom_css else "",
            )

        app.route(f"/{prefix.lstrip('/')}")(render_admin)

        @authorize
        async def ra(request):
            data = self.to_ra()

            if self.__dashboard__:
                data["dashboard"] = await self.__dashboard__(request)

            return data

        app.route(f"{prefix}/ra.json")(ra)

        async def render_admin_static(_):
            return ResponseFile(PACKAGE_DIR / "main.js")

        app.route(f"{prefix}/main.js")(render_admin_static)

        async def login(request):
            return await self.__login__(request)

        app.route(f"{prefix}/login")(login)

        async def ident(request):
            return await self.__ident__(request)

        app.route(f"{prefix}/ident")(ident)

    def route(self, path: Any, *paths: str, **params) -> Callable:
        """Route an handler."""
        if not isinstance(path, str):
            self.register_handler(path)
            return self.api.route(path)

        paths = (path, *paths)

        def wrapper(cb):
            self.register_handler(cb)
            return self.api.route(*paths, **params)(cb)

        return wrapper

    def register_handler(self, handler: Any):
        """Register an handler."""
        if isclass(handler) and issubclass(handler, AdminHandler):
            self.handlers.append(handler)

    # Authorization flow
    # ------------------

    def check_auth(self, fn: TAuth) -> TAuth:
        """Register a function to authorize current user."""
        self.auth["required"] = True
        self.api.authorize = fn
        return fn

    def login(self, fn: TAuth) -> TAuth:
        """Register a function to login current user."""
        self.auth["authorizeURL"] = f"{self.cfg.prefix}/login"
        self.__login__ = fn
        return fn

    def dashboard(self, fn: TAuth) -> TAuth:
        """Register a function to render dashboard."""
        self.__dashboard__ = fn
        return fn

    def get_identity(self, fn: TAuth) -> TAuth:
        """Register a function to identificate current user.

        User data: {id, fullName, avatar}
        """
        self.auth["identityURL"] = f"{self.cfg.prefix}/ident"
        self.__ident__ = fn
        return fn

    # Serialize to react-admin
    # -------------------------

    def to_ra(self) -> Dict[str, Any]:
        """Prepare params for react-admin."""
        handlers = self.handlers
        if self.cfg.menu_sort:
            handlers = sorted(handlers, key=lambda r: r.meta.name)

        return {
            "apiUrl": f"{self.cfg.prefix}/api",
            "auth": self.auth,
            "adminProps": {
                "title": self.cfg.title,
                "disableTelemetry": True,
                "mutationMode": self.cfg.mutation_mode,
            },
            "appBarLinks": self.cfg.app_bar_links,
            "resources": [res.to_ra() for res in handlers],
            "version": VERSION,
        }
