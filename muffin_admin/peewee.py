""" Peewee support. """
import muffin
import peewee as pw
from wtforms import fields as f

from .handler import AdminHandler


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
        return cls


class PWAdminHandler(AdminHandler, metaclass=PWAdminHandlerMeta):

    """ Peewee operations. """

    model = None
    form_meta = {}

    def get_collection(self, request):
        """ Get collection. """
        return self.model.select()

    def get_resource(self, request):
        """ Load a resource. """
        resource = request.GET.get('pk')
        if not resource:
            return None

        try:
            return self.collection.where(self.model._meta.primary_key == resource).get()
        except Exception:
            raise muffin.HTTPNotFound()

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
        if not self.resource:
            raise muffin.HTTPNotFound('Resource not found')
        self.resource.delete_instance()
