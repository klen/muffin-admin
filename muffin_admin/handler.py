""" Implement Admin interfaces. """
import muffin
import copy
import ujson as json

from muffin import Handler
from muffin.utils import abcoroutine
from wtforms import Form

from .formatters import format_value
from .filters import default_converter, PREFIX as FILTERS_PREFIX, DEFAULT


class AdminHandlerMeta(type(Handler)):

    """ Prepare admin handler. """

    def __new__(mcs, name, bases, params):
        """ Copy columns formatters to created class. """
        cls = super(AdminHandlerMeta, mcs).__new__(mcs, name, bases, params)
        cls.columns_formatters = copy.copy(cls.columns_formatters)
        return cls


class AdminHandler(Handler, metaclass=AdminHandlerMeta):

    """ Docstring here. """

    actions = None

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

    url = None

    def __init__(self):
        """ Define self templates. """
        self.template_list = self.template_list or self.app.ps.admin.cfg.template_list
        self.template_item = self.template_item or self.app.ps.admin.cfg.template_item

        # Prepare filters
        self.columns_filters = list(map(self.filters_converter, self.columns_filters))
        self.filter_form = Form(prefix=FILTERS_PREFIX)
        for flt in self.columns_filters:
            flt.bind(self.filter_form)

    @classmethod
    def connect(cls, app, *paths, methods=None, name=None, view=None):
        """ Connect to admin interface and application. """
        # Register self in admin
        if view is None:
            app.ps.admin.register(cls)
            if not paths:
                paths = ('%s/%s' % (app.ps.admin.cfg.prefix, name or cls.name),)
            cls.url = paths[0]
        return super(AdminHandler, cls).connect(app, *paths, methods=methods, name=name, view=view)

    @classmethod
    def action(cls, view):
        """ Register admin view action. """
        name = "%s-%s" % (cls.name, view.__name__)
        path = "%s/%s" % (cls.url, view.__name__)
        if cls.actions is None:
            cls.actions = []
        cls.actions.append((view.__doc__, path))
        return cls.register(path, name=name)(view)

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
        raise muffin.HTTPFound(self.url)

    @classmethod
    def columns_formatter(cls, colname):
        """ Decorator to mark a function as columns formatter. """
        def wrapper(func):
            cls.columns_formatters[colname] = func
            return func
        return wrapper

    def render_value(self, data, column):
        """ Render value. """
        renderer = self.columns_formatters.get(column, format_value)
        return renderer(self, data, column)
