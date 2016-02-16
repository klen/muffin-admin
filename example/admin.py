import random

import muffin
from muffin.utils import Struct

from example import app
from example.models import User, Message
from muffin_admin.filters import PWLikeFilter
from muffin_admin.peewee import PWAdminHandler


@app.register
class TestHandler(app.ps.admin.Handler):

    name = 'simple'
    columns = 'id', 'name', 'random'
    columns_formatters = {
        'random': lambda view, item, col: random.randint(1, 99)
    }
    columns_filters = 'name',

    def load_one(self, request):
        resource = request.GET.get('pk')
        if resource:
            return self.collection[int(resource) - 1]

    @staticmethod
    def load_many(request):
        return [
            Struct(id=1, name='test1'),
            Struct(id=2, name='test2'),
            Struct(id=3, name='test3'),
        ]


@app.register
class PWHandler1(PWAdminHandler):
    limit = 35
    model = Message
    name = 'peewee message'
    columns_labels = {'created': 'Created at'}
    columns_filters = 'active', 'status', PWLikeFilter('content')
    form_rawid_fields = 'user',


@PWHandler1.action
def bulk_delete(handler, request):
    """Bulk delete items"""
    ids = request.GET.getall('ids')
    Message.delete().where(Message.id << ids).execute()
    raise muffin.HTTPFound(handler.url)


@app.register
class PWHandler2(PWAdminHandler):
    limit = 5
    model = User
    name = 'peewee user'
    columns_labels = {'created': 'Created at'}
