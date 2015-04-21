""" Setup the plugin. """
import asyncio
import muffin
import os.path as op

from muffin.plugins import BasePlugin, PluginException
from collections import OrderedDict

from .handler import AdminHandler


PLUGIN_ROOT = op.dirname(op.abspath(__file__))


class Plugin(BasePlugin):

    """ Admin interface for Muffin Framework. """

    name = 'admin'
    defaults = {
        'prefix': '/admin',
        'name': None,
        'home': None,
    }

    Handler = AdminHandler

    def setup(self, app):
        """ Initialize the application. """
        super().setup(app)

        self.handlers = OrderedDict()

        # Connect admin static files
        app.cfg.STATIC_FOLDERS.append(op.join(PLUGIN_ROOT, 'static'))

        if 'jade' not in app.plugins:
            raise PluginException('The plugin requires Muffin-Jade installed.')

        # Connect admin templates
        app.ps.jade.options.template_folders.append(op.join(PLUGIN_ROOT, 'templates'))

        if self.options.name is None:
            self.options.name = "%s admin" % app.name.title()

        # Register a base view
        if not callable(self.options.home):
            def admin_home(request):
                yield from self.authorize(request)
                return app.ps.jade.render('admin/home.jade')
            self.options.home = admin_home

        app.register(self.options.prefix)(self.options.home)

    def register(self, handler):
        """ Ensure that handler is not registered. """
        name = handler.name.lower()
        if name in self.handlers:
            raise PluginException('Admin handler %s is already registered' % name)
        self.handlers[name] = handler
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
