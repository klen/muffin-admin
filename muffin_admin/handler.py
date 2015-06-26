""" Implement Admin interfaces. """
import asyncio
import muffin
import ujson as json

from muffin import Handler
from muffin.utils import abcoroutine
from wtforms import Form

from .formatters import format_value
from .filters import default_converter, PREFIX as FILTERS_PREFIX, DEFAULT


class AdminHandler(Handler):

    """ Docstring here. """

    # List of columns
    columns = 'id',
    columns_labels = {}
    columns_formatters = {}
    columns_filters = ()
    columns_sort = None

    # WTF form class
    form = None

    # Templates
    template_list = None
    template_item = None

    # Permissions
    can_create = True
    can_edit = True
    can_delete = True

    limit = 50

    filters_converter = default_converter

    def __init__(self, app):
        """ Define self templates. """
        super(AdminHandler, self).__init__(app)

        self.template_list = self.template_list or app.ps.admin.options.template_list
        self.template_item = self.template_item or app.ps.admin.options.template_item

        # Prepare filters
        self.columns_filters = list(map(self.filters_converter, self.columns_filters))
        self.filter_form = Form(prefix=FILTERS_PREFIX)
        for flt in self.columns_filters:
            flt.bind(self.filter_form)

    @classmethod
    def connect(cls, app, *paths, methods=None, name=None):
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
        # Authorize request
        self.auth = yield from self.authorize(request)

        # Load collection
        self.collection = yield from self.load_many(request)

        # Load resource
        self.resource = yield from self.load_one(request)

        if request.method == 'GET' and self.resource is None:

            # Filter collection
            self.collection = yield from self.filter(request)
            self.count = yield from self.count(request)

            # Sort collection
            self.columns_sort = request.GET.get('ap-sort', self.columns_sort)
            if self.columns_sort:
                reverse = self.columns_sort.startswith('-')
                self.columns_sort = self.columns_sort.lstrip('+-')
                self.collection = yield from self.sort(request, reverse=reverse)

            # Paginate collection
            try:
                self.offset = int(request.GET.get('ap-offset', 0))
                if self.limit:
                    self.collection = yield from self.paginate(request)
            except ValueError:
                pass

        return (yield from super(AdminHandler, self).dispatch(request, **kwargs))

    @abcoroutine
    def authorize(self, request):
        """ Base point for authorization. """
        return (yield from self.app.ps.admin.authorize(request))

    @abcoroutine
    def load_many(self, request):
        """ Base point for collect data. """
        return []

    @abcoroutine
    def count(self, request):
        """ Get count. """
        return len(self.collection)

    @abcoroutine
    def load_one(self, request):
        """ Base point load resource. """
        return request.GET.get('pk')

    @abcoroutine
    def filter(self, request):
        """ Filter collection. """
        collection = self.collection
        self.filter_form.process(request.GET)
        data = self.filter_form.data
        self.filter_form.active = any(o and o is not DEFAULT for o in data.values())
        for flt in self.columns_filters:
            collection = flt.apply(collection, data)
        return collection

    @abcoroutine
    def sort(self, request, reverse=False):
        """ Sort collection. """
        return sorted(
            self.collection, key=lambda o: getattr(o, self.columns_sort, 0), reverse=reverse)

    @abcoroutine
    def paginate(self, request):
        """ Paginate collection. """
        return self.collection[self.offset: self.offset + self.limit]

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

    def populate(self):
        """ Create object. """
        return object()

    @abcoroutine
    def get(self, request):
        """ Get collection of resources. """
        form = yield from self.get_form(request)
        ctx = dict(active=self, form=form, request=request)
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
