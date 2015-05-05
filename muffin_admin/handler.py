""" Implement Admin interfaces. """
import asyncio
import muffin
import ujson as json

from muffin import Handler
from muffin.utils import abcoroutine

from .formatters import format_value


class AdminHandler(Handler):

    """ Docstring here. """

    # List of columns
    columns = 'id',
    columns_labels = {}
    columns_formatters = {}

    # WTF form class
    form = None

    # Templates
    template_list = None
    template_item = None

    # Permissions
    can_create = True
    can_edit = True
    can_delete = True

    def __init__(self, app):
        """ Define self templates. """
        super(AdminHandler, self).__init__(app)

        self.template_list = self.template_list or app.ps.admin.options.template_list
        self.template_item = self.template_item or app.ps.admin.options.template_item

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
        ordering = request.GET.get('_ordering')
        if ordering:
            reverse = ordering.startswith('-')
            self.ordering = ordering.lstrip('+-')
            self.collection = self.sort_collection(self.collection, self.ordering, reverse=reverse)
        self.resource = yield from self.get_resource(request)
        return (yield from super(AdminHandler, self).dispatch(request, **kwargs))

    @abcoroutine
    def authorize(self, request):
        """ Base point for authorization. """
        auth = yield from request.app.ps.admin.authorize(request)
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
        if not self.can_create and not self.resource:
            raise muffin.HTTPForbidden()

        if not self.can_edit and self.resource:
            raise muffin.HTTPForbidden()

        resource = self.resource or self.populate()
        form.populate_obj(resource)
        return resource

    def sort_collection(self, collection, ordering, reverse=False):
        """ Sort collection. """
        return sorted(collection, key=lambda o: getattr(o, ordering, 0), reverse=reverse)

    def populate(self):
        """ Create object. """
        return object()

    @abcoroutine
    def get(self, request):
        """ Get collection of resources. """
        form = yield from self.get_form(request)
        ctx = dict(active=self, form=form)
        if self.resource:
            return self.app.ps.jinja2.render(self.template_item, **ctx)
        return self.app.ps.jinja2.render(self.template_list, **ctx)

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
        renderer = self.columns_formatters.get(column, format_value)
        return renderer(self, data, column)
