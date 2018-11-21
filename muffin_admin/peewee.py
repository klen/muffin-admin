"""Peewee support."""
import muffin
import peewee as pw

from wtforms import fields as f, Form, StringField

from .filters import Filter
from .handler import AdminHandler


try:
    from wtfpeewee.orm import ModelConverter, FieldInfo, model_fields

    ModelConverter.defaults[pw.DateField] = f.DateField
    ModelConverter.defaults[pw.DateTimeField] = f.DateTimeField

    from muffin_peewee.fields import JSONField
    ModelConverter.defaults[JSONField] = f.TextAreaField

except ImportError:
    model_form = ModelConverter = model_fields = None


def pw_converter(handler, flt):
    """Convert column name to filter."""
    import peewee as pw

    if isinstance(flt, Filter):
        return flt

    model = handler.model
    field = getattr(model, flt)

    if isinstance(field, pw.BooleanField):
        return PWBoolFilter(flt)

    if field.choices:
        choices = [(Filter.default, '---')] + list(field.choices)
        return PWChoiceFilter(flt, choices=choices)

    return PWFilter(flt)


class RawIDField(StringField):

    """Simple Raw ID field implementation."""

    def __init__(self, field, *args, **kwargs):
        """Store model field."""
        self.field = field
        super(RawIDField, self).__init__(*args, **kwargs)

    def process(self, *args, **kwargs):
        """Get a description."""
        super(RawIDField, self).process(*args, **kwargs)
        if self.object_data:
            self.description = self.description or str(self.object_data)

    def _value(self):
        """Get field value."""
        if self.data is not None:
            value = self.data._data.get(self.field.to_field.name)
            return str(value)
        return ''


class PWAdminHandlerMeta(type(AdminHandler)):

    """Fill name from model."""

    def __new__(mcs, name, bases, params):
        """Create a class."""
        model = params.get('model')
        if model:
            params.setdefault('name', model._meta.db_table)
            params.setdefault('columns', [f.name for f in model._meta.sorted_fields])
            # Peewee 3+
            #  params.setdefault('name', model._meta.table_name)
            #  params.setdefault('columns', model._meta.sorted_field_names)

        cls = super(PWAdminHandlerMeta, mcs).__new__(mcs, name, bases, params)
        if not cls.form and cls.model and model_fields and ModelConverter:
            cls.__converter = ModelConverter(
                additional={pw.ForeignKeyField: cls.handle_fk}, overrides=cls.form_overrides)

            fields = model_fields(
                cls.model, allow_pk=cls.form_allow_pk, only=cls.form_only,
                exclude=cls.form_exclude, field_args=cls.form_field_args,
                converter=cls.__converter)
            fields.update(cls.form_fields)
            cls.form = type("%sForm" % cls.model.__name__, (cls.form_base_class,), fields)

        if cls.columns_exclude:
            cls.columns = [col for col in cls.columns if col not in cls.columns_exclude]

        return cls

    def handle_fk(cls, model, field, **kwargs): # noqa
        converter = cls.__converter
        if field.name not in cls.form_rawid_fields:
            return converter.handle_foreign_key(model, field, **kwargs)
        return FieldInfo(field.name, RawIDField(field, **kwargs))


class PWAdminHandler(AdminHandler, metaclass=PWAdminHandlerMeta):

    """Peewee operations."""

    model = None

    columns_exclude = ()
    columns_sort = '-id'

    # Base form class to extend from.
    form_base_class = Form

    # Allow pk editing.
    form_allow_pk = False

    # An optional iterable with the property names that should be included in the form.
    form_only = None

    # An optional iterable with the property names that should be excluded from the form
    form_exclude = None

    # Form fields
    form_fields = {}

    # An optional dictionary of field names mapping to keyword arguments used to construct field
    form_field_args = None

    # RawID fields
    form_rawid_fields = ()

    # Override form fields
    form_overrides = {}

    methods = 'get', 'post', 'delete'

    filters_converter = pw_converter

    def load_many(self, request):
        """Get collection."""
        return self.model.select()

    def load_one(self, request):
        """Load a resource."""
        resource = request.query.get('pk')
        if not resource:
            return None

        try:
            return self.collection.where(self.model._meta.primary_key == resource).get()
        except Exception:
            raise muffin.HTTPNotFound()

    def sort(self, request, reverse=False):
        """Sort current collection."""
        field = self.model._meta.fields.get(self.columns_sort)
        if not field:
            return self.collection

        if reverse:
            field = field.desc()

        return self.collection.order_by(field)

    def paginate(self, request):
        """Paginate collection."""
        return self.collection.offset(self.offset).limit(self.limit)

    def count(self, request):
        """Get count."""
        return self.collection.count()

    def populate(self):
        """Create object."""
        return self.model()

    def save_form(self, form, request, **resources):
        """Save self form."""
        resource = yield from super(PWAdminHandler, self).save_form(form, request, **resources)
        resource.save()
        return resource

    def delete(self, request):
        """Delete an item."""
        if not self.can_delete:
            raise muffin.HTTPMethodNotAllowed()

        if not self.resource:
            raise muffin.HTTPNotFound(reason='Resource not found')

        self.resource.delete_instance()

    def get_pk(self, item):
        """Get PK field."""
        return item._get_pk_value()
        #  Peewee 3+
        #  return item._pk


class PWFilter(Filter):

    """Base filter for Peewee handlers."""

    def __init__(self, name, model_field=None, **field_kwargs):
        """Store name and mode."""
        super(PWFilter, self).__init__(name, **field_kwargs)
        self.model_field = model_field

    def apply(self, query, data):
        """Filter a query."""
        field = self.model_field or query.model_class._meta.fields.get(self.name)
        if not field or self.name not in data:
            return query
        value = self.value(data)
        if value is self.default:
            return query
        value = field.db_value(value)
        return self.filter_query(query, field, value)

    @staticmethod
    def filter_query(query, field, value):
        """Filter a query."""
        return query.where(field == value)


class PWLikeFilter(PWFilter):

    """Filter query by value."""

    def filter_query(self, query, field, value):
        """Filter a query."""
        return query.where(field ** "%{}%".format(value.lower()))


class PWBoolFilter(PWFilter):

    """Boolean filter."""

    field = f.SelectField
    field_kwargs = {
        'choices': (
            (Filter.default, '---'),
            (1, 'yes'),
            (0, 'no'),
        )
    }

    def value(self, data):
        """Get value from data."""
        value = data.get(self.name)
        if value:
            return int(value)
        return self.default


class PWChoiceFilter(PWFilter):

    """Select field."""

    field = f.SelectField

#  pylama:ignore=C0202,R0201,W0201,E0202,E1102,E1120
