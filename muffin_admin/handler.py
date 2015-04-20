""" Implement Admin interfaces. """
import asyncio

from muffin_rest import RESTHandler
import ujson
from .formatters import format_value


class AdminHandler(RESTHandler):

    """ Docstring here. """

    columns = '#',
    template = 'admin/list.jade'
    methods = 'get', 'post', 'delete'

    @classmethod
    def connect(cls, app, *paths, name=None):
        """ Connect to admin interface and application. """
        admin = app.ps.admin
        admin.handlers.append(cls)
        params = {
            'prefix': admin.options.prefix,
            'name': name or cls.name.lower(),
        }
        paths = paths or (
            '%(prefix)s/%(name)s' % params,
            '%(prefix)s/%(name)s/{%(name)s}' % params,
        )
        return super(AdminHandler, cls).connect(app, *paths, name=name)

    @asyncio.coroutine
    def make_response(self, request, response):
        """ Render response. """
        if request.method == 'GET':
            form = (yield from self.get_form(request)) if self.form else None
            response = self.app.ps.jade.render(
                self.template, active=self, data=response, form=form, json=ujson.dumps)
        return (yield from super(AdminHandler, self).make_response(request, response))

    def render_value(self, data, column):
        """ Render value. """
        return format_value(self, data, data.get(column))

    def render_form_template(self, form):
        for field in form:
            import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
