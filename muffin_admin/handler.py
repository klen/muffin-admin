"""Implement Admin interfaces."""
import muffin
import copy

from aiohttp.web import StreamResponse
from muffin import Handler
from muffin.utils import json
from wtforms import Form

from .formatters import format_value
from .filters import default_converter, PREFIX as FILTERS_PREFIX, DEFAULT


class AdminHandlerMeta(type(Handler)):
    """Prepare admin handler."""

    def __new__(mcs, name, bases, params):
        """Copy columns formatters to created class."""
        cls = super(AdminHandlerMeta, mcs).__new__(mcs, name, bases, params)
        cls.actions = []
        cls.global_actions = []
        cls.name = cls.name.replace(' ', '_')
        cls.columns_formatters = copy.copy(cls.columns_formatters)
        return cls


class AdminHandler(Handler, metaclass=AdminHandlerMeta):
    """Base admin handler. Inherit from this class any other implementation."""

    # List of columns
    columns = 'id',
    columns_labels = {}
    columns_formatters = {}
    columns_formatters_csv = {}
    columns_filters = ()
    columns_sort = None
    columns_csv = None

    # WTF form class
    form = None

    # Templates
    template_list = None
    template_item = None

    # Permissions
    can_create = True
    can_edit = True
    can_delete = True

    # Group
    group = ''

    limit = 50

    filters_converter = default_converter

    url = None

    def __init__(self):
        """Define self templates."""
        self.template_list = self.template_list or self.app.ps.admin.cfg.template_list
        self.template_item = self.template_item or self.app.ps.admin.cfg.template_item

        # Prepare filters
        self.columns_filters = list(map(self.filters_converter, self.columns_filters))
        self.filter_form = Form(prefix=FILTERS_PREFIX)
        for flt in self.columns_filters:
            flt.bind(self.filter_form)

    @classmethod
    def bind(cls, app, *paths, methods=None, name=None, view=None):
        """Connect to admin interface and application."""
        # Register self in admin
        if view is None:
            app.ps.admin.register(cls)
            if not paths:
                paths = ('%s/%s' % (app.ps.admin.cfg.prefix, name or cls.name),)
            cls.url = paths[0]
        return super(AdminHandler, cls).bind(app, *paths, methods=methods, name=name, view=view)

    @classmethod
    def action(cls, view):
        """Register admin view action."""
        name = "%s:%s" % (cls.name, view.__name__)
        path = "%s/%s" % (cls.url, view.__name__)
        cls.actions.append((view.__doc__, path))
        return cls.register(path, name=name)(view)

    @classmethod
    def global_action(cls, view):
        """Register admin view action."""
        name = "%s:%s" % (cls.name, view.__name__)
        path = "%s/%s" % (cls.url, view.__name__)
        cls.global_actions.append((view.__doc__, path))
        return cls.register(path, name=name)(view)

    async def dispatch(self, request, **kwargs):
        """Dispatch a request."""
        # Authorize request
        self.auth = await self.authorize(request)

        # Load collection
        self.collection = await self.load_many(request)

        # Load resource
        self.resource = await self.load_one(request)

        if request.method == 'GET' and self.resource is None:

            # Filter collection
            self.collection = await self.filter(request)

            # Sort collection
            self.columns_sort = request.query.get('ap-sort', self.columns_sort)
            if self.columns_sort:
                reverse = self.columns_sort.startswith('-')
                self.columns_sort = self.columns_sort.lstrip('+-')
                self.collection = await self.sort(request, reverse=reverse)

            if 'csv' in request.query:
                return await self.render_csv(request)

            # Paginate collection
            try:
                self.offset = int(request.query.get('ap-offset', 0))
                if self.limit:
                    self.count = await self.count(request)
                    self.collection = await self.paginate(request)
            except ValueError:
                pass

        return await super(AdminHandler, self).dispatch(request, **kwargs)

    async def authorize(self, request):
        """Base point for authorization."""
        return await self.app.ps.admin.authorize(request)

    async def load_many(self, request):
        """Base point for collect data."""
        return []

    async def count(self, request):
        """Get count."""
        return len(self.collection)

    async def load_one(self, request):
        """Base point load resource."""
        return request.query.get('pk')

    async def filter(self, request):
        """Filter collection."""
        collection = self.collection
        self.filter_form.process(request.query)
        data = self.filter_form.data
        self.filter_form.active = any(o and o is not DEFAULT for o in data.values())
        for flt in self.columns_filters:
            try:
                collection = flt.apply(collection, data)
            # Invalid filter value
            except ValueError:
                continue
        return collection

    async def sort(self, request, reverse=False):
        """Sort collection."""
        return sorted(
            self.collection, key=lambda o: getattr(o, self.columns_sort, 0), reverse=reverse)

    async def paginate(self, request):
        """Paginate collection."""
        return self.collection[self.offset: self.offset + self.limit]

    async def get_form(self, request):
        """Base point load resource."""
        if not self.form:
            return None
        formdata = await request.post()
        return self.form(formdata, obj=self.resource)

    async def save_form(self, form, request, **resources):
        """Save self form."""
        if not self.can_create and not self.resource:
            raise muffin.HTTPForbidden()

        if not self.can_edit and self.resource:
            raise muffin.HTTPForbidden()

        resource = self.resource or self.populate()
        form.populate_obj(resource)
        return resource

    def populate(self):
        """Create object."""
        return object()

    async def get(self, request):
        """Get collection of resources."""
        form = await self.get_form(request)
        ctx = dict(active=self, form=form, request=request)
        if self.resource:
            return self.app.ps.jinja2.render(self.template_item, **ctx)
        return self.app.ps.jinja2.render(self.template_list, **ctx)

    async def post(self, request):
        """Create/Edit items."""
        form = await self.get_form(request)
        if not form.validate():
            raise muffin.HTTPBadRequest(
                text=json.dumps(form.errors), content_type='application/json')
        await self.save_form(form, request)
        raise muffin.HTTPFound(self.url)

    @classmethod
    def columns_formatter(cls, colname):
        """Decorator to mark a function as columns formatter."""
        def wrapper(func):
            cls.columns_formatters[colname] = func
            return func
        return wrapper

    def render_value(self, data, column):
        """Render value."""
        renderer = self.columns_formatters.get(column, format_value)
        return renderer(self, data, column)

    def render_value_csv(self, data, column):
        """Render value for CSV."""
        renderer = self.columns_formatters_csv.get(column, csv_format_value)
        return renderer(self, data, column)

    def get_pk(self, item):
        """Get PK field."""
        return getattr(item, 'pk', item)

    async def render_csv(self, request):
        """Render CSV."""
        res = StreamResponse(headers={
            "Content-Type": "text/csv",
            "Content-Disposition": 'attachment; filename="%s.csv"' % self.name,
        })
        await res.prepare(request)
        columns = self.columns_csv or self.columns
        await res.write(
            ("%s\n" % ';'.join([
                self.columns_labels.get(col, col.title()) for col in columns]))
            .encode('utf-8')
        )
        count = await self.count(request)
        for offset in range(0, count, self.limit):
            self.offset = offset
            page = await self.paginate(request)
            for item in page:
                await res.write(
                    ("%s\n" % ';'.join([self.render_value_csv(item, col) for col in columns]))
                    .encode('utf-8')
                )

        await res.write_eof()
        return res


def csv_format_value(handler, item, column):
    """Format CSV."""
    for attr in column.split('.'):
        item = getattr(item, attr, None)
    return str(item)

#  pylama:ignore=C0202,R0201,W0201,E0202,E1102
