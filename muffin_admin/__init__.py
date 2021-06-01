"""Plugin meta information."""

from .plugin import Plugin # noqa

# Package information
# ===================

__version__ = "1.7.2"
__project__ = "muffin-admin"
__author__ = "Kirill Klenov <horneds@gmail.com>"
__license__ = "MIT"


from .handler import AdminHandler

try:
    from .peewee import PWAdminHandler, PWFilter
except ImportError:
    pass

try:
    from .sqlalchemy import SAAdminHandler, SAFilter
except ImportError:
    pass


# pylama: ignore=W0611
