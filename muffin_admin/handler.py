""" Implement Admin interfaces. """
import asyncio
import muffin
import ujson as json

from muffin import Handler
from muffin.utils import abcoroutine

from .formatters import format_value


class AdminHandler(Handler):

    """ Docstring here. """

    columns = '#',
    form = None
    template_list = 'admin/list.jade'
    template_item = 'admin/item.jade'

    @classmethod
    def connect(cls, app, *paths, name=None):
        """ Connect to admin interface and application. """
        # Register self in admin
        app.ps.admin.register(cls)

        @asyncio.coroutine
        def view(request):
            handler = cls(app)
            response = yield from handler.dispatch(request)
            return response

        paths = paths or (
            '%s/%s' % (app.ps.admin.options.prefix, name or cls.name),
        )

        for path in paths:
            app.router.add_route('*', path, view)

    @abcoroutine
    def dispatch(self, request, **kwargs):
        """ Dispatch a request. """
        self.auth = yield from self.authorize(request)
        self.collection = yield from self.get_collection(request)
        self.resource = yield from self.get_resource(request)
        return (yield from super(AdminHandler, self).dispatch(request, **kwargs))

    @abcoroutine
    def authorize(self, request):
        """ Base point for authorization. """
        app = request.app
        admin = request.app.ps.admin
        auth = yield from admin.authorize(request, app=app)
        return auth

    @abcoroutine
    def get_collection(self, request):
        """ Base point for collect data. """
        return []

    @abcoroutine
    def get_resource(self, request):
        """ Base point load resource. """
        return request.GET.get('pk')

    @abcoroutine
    def get_form(self, request):
        """ Base point load resource. """
        if not self.form:
            return None
        formdata = yield from request.post()
        return self.form(formdata, obj=self.resource)

    @abcoroutine
    def save_form(self, form, request, **resources):
        """ Save self form. """
        resource = self.resource or self.populate()
        form.populate_obj(resource)
        return resource

    def populate(self):
        """ Create object. """
        return object()

    @abcoroutine
    def get(self, request):
        """ Get collection of resources. """
        form = yield from self.get_form(request)
        ctx = dict(active=self, form=form)
        if self.resource:
            return self.app.ps.jade.render(self.template_item, **ctx)
        return self.app.ps.jade.render(self.template_list, **ctx)

    @abcoroutine
    def post(self, request):
        """ Create/Edit items. """
        form = yield from self.get_form(request)
        if not form.validate():
            raise muffin.HTTPBadRequest(
                text=json.dumps(form.errors), content_type='application/json')
        yield from self.save_form(form, request)
        raise muffin.HTTPFound("%s/%s" % (self.app.ps.admin.options.prefix, self.name))

    def render_value(self, data, column):
        """ Render value. """
        return format_value(self, data, getattr(data, column))
