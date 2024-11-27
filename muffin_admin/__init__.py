"""Plugin meta information."""

from contextlib import suppress

from .handler import AdminHandler
from .plugin import Plugin

with suppress(ImportError):
    from .peewee import PWAdminHandler, PWFilter

with suppress(ImportError):
    from .sqlalchemy import SAAdminHandler, SAFilter


__all__ = (
    "AdminHandler",
    "PWAdminHandler",
    "PWFilter",
    "Plugin",
    "SAAdminHandler",
    "SAFilter",
)
