"""Peewee support."""
import muffin
import peewee as pw

from wtforms import fields as f, Form, StringField

from .filters import pw_converter
from .handler import AdminHandler


try:
    from wtfpeewee.orm import model_form, ModelConverter

    ModelConverter.defaults[pw.DateField] = f.DateField
    ModelConverter.defaults[pw.DateTimeField] = f.DateTimeField

    from muffin_peewee.fields import JSONField
    ModelConverter.defaults[JSONField] = f.TextAreaField

except ImportError:
    model_form = None
    ModelConverter = None


class RawIDField(StringField):

    """Simple Raw ID field implementation."""

    def process(self, *args, **kwargs):
        """Get a description."""
        super(RawIDField, self).process(*args, **kwargs)
        if self.object_data:
            self.description = self.description or str(self.object_data)

    def _value(self):
        """Get field value."""
        return str(self.data._get_pk_value()) if self.data is not None else ''


class PWAdminHandlerMeta(type(AdminHandler)):

    """Fill name from model."""

    def __new__(mcs, name, bases, params):
        """Create a class."""
        model = params.get('model')
        if model:
            params.setdefault('name', model._meta.db_table)
            params.setdefault('columns', [f.name for f in model._meta.sorted_fields])

        cls = super(PWAdminHandlerMeta, mcs).__new__(mcs, name, bases, params)
        if not cls.form and cls.model and model_form and ModelConverter:
            for field in cls.form_rawid_fields:
                cls.form_overrides[field] = RawIDField

            converter = ModelConverter(overrides=cls.form_overrides)
            cls.form = model_form(
                cls.model,
                base_class=cls.form_base_class,
                allow_pk=cls.form_allow_pk, only=cls.form_only, exclude=cls.form_exclude,
                field_args=cls.form_field_args, converter=converter)

        if cls.columns_exclude:
            cls.columns = [col for col in cls.columns if col not in cls.columns_exclude]

        return cls


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
        resource = request.GET.get('pk')
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

#  pylama:ignore=C0202,R0201,W0201,E0202,E1102,E1120
