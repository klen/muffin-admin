"""Plugin meta information."""

# Package information
# ===================

__version__ = "1.32.6"
__project__ = "muffin-admin"
__author__ = "Kirill Klenov <horneds@gmail.com>"
__license__ = "MIT"

from .handler import AdminHandler
from .plugin import Plugin  # noqa

try:
    from .peewee import PWAdminHandler, PWFilter
except ImportError:
    pass

try:
    from .sqlalchemy import SAAdminHandler, SAFilter
except ImportError:
    pass


__all__ = (
    "AdminHandler",
    "PWAdminHandler",
    "PWFilter",
    "SAAdminHandler",
    "SAFilter",
    "Plugin",
)
