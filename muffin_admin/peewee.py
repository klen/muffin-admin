""" Peewee support. """
import muffin
from muffin_rest.peewee import PWRESTHandlerMeta, PWRESTHandler

from .handler import AdminHandler


class PWAdminHandlerMeta(PWRESTHandlerMeta):

    """ Fill name from model. """

    def __new__(mcs, name, bases, params):
        """ Create a class. """
        model = params.get('model')
        if model:
            params.setdefault('name', model._meta.db_table)
            params.setdefault('columns', [n for (n, _) in model._meta.get_sorted_fields()])

        return super(PWAdminHandlerMeta, mcs).__new__(mcs, name, bases, params)


class PWAdminHandler(AdminHandler, PWRESTHandler, metaclass=PWAdminHandlerMeta):

    """ Peewee operations. """

    model = None

    def get_many(self, request):
        """ Get collection. """
        return self.model.select()

    def get_one(self, request):
        """ Load a resource. """
        resource = request.match_info.get(self.name)
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
