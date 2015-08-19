import pytest
import muffin


@pytest.fixture(scope='session')
def app(loop):
    app = muffin.Application(
        'admin', loop=loop,

        PLUGINS=['muffin_jinja2', 'muffin_admin', 'muffin_peewee'],

        PEEWEE_CONNECTION='sqlite:///:memory:'
    )

    @app.register
    class Test(app.ps.admin.Handler):

        columns = 'id', 'name'

        def load_one(self, request):
            resource = request.match_info.get(self.name)
            if resource:
                return self.collection[int(resource) - 1]

        def load_many(self, request):
            return [
                muffin.utils.Struct(id=1, name='test1'),
                muffin.utils.Struct(id=2, name='test2'),
                muffin.utils.Struct(id=3, name='test3'),
            ]

    @app.ps.admin.authorization
    def ensure_code_in_get(request):
        """ Simple fake authentication process. """
        if 'auth' not in request.GET:
            raise muffin.HTTPForbidden()
        return True

    return app


def test_home(client):
    response = client.get('/admin', status=403)
    assert response.status_code == 403

    response = client.get('/admin?auth=1')
    assert response.status_code == 200


def test_handler(app, client):
    assert app.ps.admin.handlers

    th = app.ps.admin.handlers['test']
    assert th.name == 'test'

    response = client.get('/admin/test', status=403)
    assert response.status_code == 403

    response = client.get('/admin/test?auth=1')
    assert response.status_code == 200
    assert 'test1' in response.text
    assert 'test2' in response.text
    assert 'test3' in response.text


def test_peewee(app, client):
    import peewee as pw
    from muffin_peewee.fields import JSONField

    @app.ps.peewee.register
    class Model(app.ps.peewee.TModel):

        active = pw.BooleanField()
        content = pw.CharField()
        config = JSONField(default={})

    @app.ps.peewee.register
    class Model2(app.ps.peewee.TModel):
        pass

    Model.create_table()
    Model2.create_table()

    from muffin_admin.peewee import PWAdminHandler

    @app.register
    class ModelHandler(PWAdminHandler):
        model = Model
        columns_exclude = 'created',
        columns_filters = 'content',

    assert ModelHandler.columns
    assert ModelHandler.columns == ['id', 'active', 'content', 'config']
    assert ModelHandler.name == 'model'
    assert ModelHandler.form
    assert ModelHandler.form.config
    assert ModelHandler.can_create
    assert ModelHandler.can_edit
    assert ModelHandler.can_delete
    assert ModelHandler.columns_formatters is not PWAdminHandler.columns_formatters

    # Make admin handler dynamically
    app.ps.admin.register(Model2, can_delete=False)
    handler = app.ps.admin.handlers['model2']
    assert handler.model == Model2
    assert handler.can_delete is False

    from mixer.backend.peewee import Mixer
    mixer = Mixer(commit=True)
    models = mixer.cycle(3).blend(Model)

    response = client.get('/admin/model?auth=1')
    assert models[0].content in response.text
    assert models[1].content in response.text
    assert models[2].content in response.text

    response = client.get('/admin/model?pk=1&auth=1')
    assert 'created' in response.text

    response = client.post('/admin/model?pk=1&auth=1', {
        'content': 'new content'
    })
    assert response.status_code == 302

    response = client.delete('/admin/model?pk=1&auth=1')
    assert not Model.select().where(Model.id == 1).exists()

    response = client.get('/admin/model2?auth=1')
    assert response.status_code == 200

    response = client.get('/admin/model?auth=1&af-content=%s' % models[1].content)
    assert models[1].content in response.text
    assert not models[2].content in response.text
