from example import app
from muffin.utils import Structure
from example.models import Test
from muffin_admin.peewee import PWAdminHandler


@app.register
class TestHandler(app.ps.admin.Handler):

    name = 'one'
    columns = 'id', 'name'

    def get_one(self, request):
        resource = request.match_info.get(self.name)
        if resource:
            return self.collection[int(resource) - 1]

    def get_many(self, request):
        return [
            Structure(id=1, name='test1'),
            Structure(id=2, name='test2'),
            Structure(id=3, name='test3'),
        ]


@app.register
class PWHandler(PWAdminHandler):

    model = Test
