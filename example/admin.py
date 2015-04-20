from example import app
from muffin.utils import Structure
from example.models import Test
from muffin_admin.peewee import PWAdminHandler


@app.register
class TestHandler(app.ps.admin.Handler):

    name = 'simple'
    columns = 'id', 'name'

    def get_resource(self, request):
        resource = request.GET.get('pk')
        if resource:
            return self.collection[int(resource) - 1]

    def get_collection(self, request):
        return [
            Structure(id=1, name='test1'),
            Structure(id=2, name='test2'),
            Structure(id=3, name='test3'),
        ]


@app.register
class PWHandler(PWAdminHandler):

    model = Test
    name = 'peewee'
