""" Setup the plugin. """
import asyncio
import muffin
import os.path as op

from muffin.plugins import BasePlugin, PluginException
from collections import OrderedDict
import urllib.parse as urlparse

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

        'template_list': 'admin/list.html',
        'template_item': 'admin/item.html',
        'template_home': 'admin/home.html',
    }

    Handler = AdminHandler

    def setup(self, app):
        """ Initialize the application. """
        super().setup(app)

        self.handlers = OrderedDict()

        if 'jinja2' not in app.plugins:
            raise PluginException('The plugin requires Muffin-Jinja2 plugin installed.')

        # Connect admin templates
        app.ps.jinja2.options.template_folders.append(op.join(PLUGIN_ROOT, 'templates'))

        @app.ps.jinja2.filter
        def admtest(value, a, b=None):
            return a if value else b

        @app.ps.jinja2.filter
        def admeq(a, b, result=True):
            return result if a == b else not result

        @app.ps.jinja2.register
        def admurl(request, prefix):
            qs = {k: v for k, v in request.GET.items() if not k.startswith(prefix)}
            if not qs:
                qs = {'ap': 0}
            return "%s?%s" % (request.path, urlparse.urlencode(qs))

        if self.options.name is None:
            self.options.name = "%s admin" % app.name.title()

        # Register a base view
        if not callable(self.options.home):

            def admin_home(request):
                yield from self.authorize(request)
                return app.ps.jinja2.render(self.options.template_home, active=None)

            self.options.home = admin_home

        app.register(self.options.prefix)(self.options.home)

    def register(self, *handlers):
        """ Ensure that handler is not registered. """
        for handler in handlers:

            if issubclass(handler, PWModel):
                handler = type(
                    handler._meta.db_table.title() + 'Admin',
                    (PWAdminHandler,), dict(model=handler))
                self.app.register(handler)

            else:

                name = handler.name.lower()
                if name in self.handlers:
                    raise PluginException('Admin handler %s is already registered' % name)
                self.handlers[name] = handler

        else:
            return handler

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
