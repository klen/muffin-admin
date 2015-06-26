""" Peewee support. """
import muffin
import peewee as pw
from wtforms import fields as f

from .handler import AdminHandler
from .filters import pw_converter


try:
    from wtfpeewee.orm import model_form, ModelConverter

    ModelConverter.defaults[pw.DateField] = f.DateField
    ModelConverter.defaults[pw.DateTimeField] = f.DateTimeField

except ImportError:
    model_form = None


class PWAdminHandlerMeta(type(AdminHandler)):

    """ Fill name from model. """

    def __new__(mcs, name, bases, params):
        """ Create a class. """
        model = params.get('model')
        if model:
            params.setdefault('name', model._meta.db_table)
            params.setdefault('columns', [n for (n, _) in model._meta.get_sorted_fields()])

        cls = super(PWAdminHandlerMeta, mcs).__new__(mcs, name, bases, params)
        if not cls.form and cls.model and model_form:
            cls.form = model_form(cls.model, **cls.form_meta)

        if cls.columns_exclude:
            cls.columns = [col for col in cls.columns if col not in cls.columns_exclude]

        return cls


class PWAdminHandler(AdminHandler, metaclass=PWAdminHandlerMeta):

    """ Peewee operations. """

    model = None

    columns_exclude = ()
    columns_sort = '-id'

    form_meta = {}

    methods = 'get', 'post', 'delete'

    filters_converter = pw_converter

    def load_many(self, request):
        """ Get collection. """
        return self.model.select()

    def load_one(self, request):
        """ Load a resource. """
        resource = request.GET.get('pk')
        if not resource:
            return None

        try:
            return self.collection.where(self.model._meta.primary_key == resource).get()
        except Exception:
            raise muffin.HTTPNotFound()

    def sort(self, request, reverse=False):
        """ Order a current collection. """
        field = self.model._meta.fields.get(self.columns_sort)
        if not field:
            return self.collection

        if reverse:
            field = field.desc()

        return self.collection.order_by(field)

    def paginate(self, request):
        """ Paginate collection. """
        return self.collection.offset(self.offset).limit(self.limit)

    def count(self, request):
        """ Get count. """
        return self.collection.count()

    def populate(self):
        """ Create object. """
        return self.model()

    def save_form(self, form, request, **resources):
        """ Save self form. """
        resource = yield from super(PWAdminHandler, self).save_form(form, request, **resources)
        resource.save()
        return resource

    def delete(self, request):
        """ Delete an item. """
        if not self.can_delete:
            raise muffin.HTTPMethodNotAllowed()

        if not self.resource:
            raise muffin.HTTPNotFound('Resource not found')

        self.resource.delete_instance()
