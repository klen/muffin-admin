""" Setup the plugin. """
import asyncio
import os.path as op
import urllib.parse as urlparse
from collections import OrderedDict

import muffin
from muffin.plugins import BasePlugin, PluginException
from muffin_jinja2 import Plugin as JPlugin
from muffin_babel import Plugin as BPlugin

from .handler import AdminHandler


try:
    from .peewee import PWAdminHandler, pw
    PWModel = pw.Model
except Exception:
    PWModel = None


PLUGIN_ROOT = op.dirname(op.abspath(__file__))


class Plugin(BasePlugin):

    """ Admin interface for Muffin Framework. """

    name = 'admin'
    defaults = {
        'prefix': '/admin',
        'name': None,
        'home': None,
        'i18n': False,

        'template_list': 'admin/list.html',
        'template_item': 'admin/item.html',
        'template_home': 'admin/home.html',
    }
    dependencies = {'jinja2': JPlugin}

    Handler = AdminHandler

    def setup(self, app):
        """ Initialize the application. """
        super().setup(app)

        self.handlers = OrderedDict()

        # Connect admin templates
        app.ps.jinja2.cfg.template_folders.append(op.join(PLUGIN_ROOT, 'templates'))

        @app.ps.jinja2.filter
        def admtest(value, a, b=None):
            return a if value else b

        @app.ps.jinja2.filter
        def admeq(a, b, result=True):
            return result if a == b else not result

        @app.ps.jinja2.register
        def admurl(request, prefix):
            qs = {k: v for k, v in request.query.items() if not k.startswith(prefix)}
            if not qs:
                qs = {'ap': 0}
            return "%s?%s" % (request.path, urlparse.urlencode(qs))

        if self.cfg.name is None:
            self.cfg.name = "%s admin" % app.name.title()

        # Register a base view
        if not callable(self.cfg.home):

            def admin_home(request):
                yield from self.authorize(request)
                return app.ps.jinja2.render(self.cfg.template_home, active=None)

            self.cfg.home = admin_home

        app.register(self.cfg.prefix)(self.cfg.home)

        if not self.cfg.i18n:
            app.ps.jinja2.env.globals.update({
                '_': lambda s: s,
                'gettext': lambda s: s,
                'ngettext': lambda s, p, n: (n != 1 and (p,) or (s,))[0],
            })

            return

        if 'babel' not in app.ps or not isinstance(app.ps.babel, BPlugin):
            raise PluginException(
                'Plugin `%s` requires for plugin `%s` to be installed to the application.' % (
                    self.name, BPlugin))

        # Connect admin locales
        app.ps.babel.cfg.locales_dirs.append(op.join(PLUGIN_ROOT, 'locales'))
        if not app.ps.babel.locale_selector_func:
            app.ps.babel.locale_selector_func = app.ps.babel.select_locale_by_request

    def register(self, *handlers, **params):
        """ Ensure that handler is not registered. """
        for handler in handlers:

            if issubclass(handler, PWModel):
                handler = type(
                    handler._meta.db_table.title() + 'Admin',
                    (PWAdminHandler,), dict(model=handler, **params))
                self.app.register(handler)
                continue

            self.handlers[handler.name] = handler

    def authorization(self, func):
        """ Define a authorization process. """
        if self.app is None:
            raise PluginException('The plugin must be installed to application.')

        self.authorize = muffin.to_coroutine(func)
        return func

    @asyncio.coroutine
    def authorize(self, request):
        """ Default authorization. """
        return True
