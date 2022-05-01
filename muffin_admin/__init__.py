"""Plugin meta information."""

from .plugin import Plugin # noqa

# Package information
# ===================

__version__ = "1.31.3"
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


__all__ = 'AdminHandler', 'PWAdminHandler', 'PWFilter', 'SAAdminHandler', 'SAFilter', 'Plugin'
