from example import app
from muffin.utils import Structure
import random
from example.models import Test
from muffin_admin.peewee import PWAdminHandler
from muffin_admin.filters import PWLikeFilter


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

    def load_many(self, request):
        return [
            Structure(id=1, name='test1'),
            Structure(id=2, name='test2'),
            Structure(id=3, name='test3'),
        ]


@app.register
class PWHandler(PWAdminHandler):

    model = Test
    name = 'peewee'
    columns_labels = {'created': 'Created at'}
    columns_filters = 'active', 'status', PWLikeFilter('content')
    limit = 5
