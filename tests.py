import pytest
import muffin


@pytest.fixture(scope='session')
def app(loop):
    app = muffin.Application(
        'admin', loop=loop,

        PLUGINS=['muffin_jade', 'muffin_admin', 'muffin_peewee'],

        PEEWEE_CONNECTION='sqlite:///:memory:'
    )

    @app.register
    class Test(app.ps.admin.Handler):

        columns = 'id', 'name'

        def get_one(self, request):
            resource = request.match_info.get(self.name)
            if resource:
                return self.collection[int(resource) - 1]

        def get_many(self, request, **resources):
            return [
                muffin.utils.Structure(id=1, name='test1'),
                muffin.utils.Structure(id=2, name='test2'),
                muffin.utils.Structure(id=3, name='test3'),
            ]

    return app


def test_home(client):
    response = client.get('/admin')
    assert response.status_code == 200


def test_handler(app, client):
    assert app.ps.admin.handlers

    [th] = app.ps.admin.handlers
    assert th.name == 'test'

    response = client.get('/admin/test')
    assert response.status_code == 200
    assert 'test1' in response.text
    assert 'test2' in response.text
    assert 'test3' in response.text


def test_peewee(app, client):
    import peewee as pw

    @app.ps.peewee.register
    class Model(app.ps.peewee.TModel):

        active = pw.BooleanField()
        content = pw.CharField()

    Model.create_table()

    from muffin_admin.peewee import PWAdminHandler

    @app.register
    class ModelHandler(PWAdminHandler):
        model = Model

    assert ModelHandler.columns
    assert ModelHandler.name == 'model'
    assert ModelHandler.form

    from mixer.backend.peewee import Mixer
    mixer = Mixer(commit=True)
    models = mixer.cycle(3).blend(Model)

    response = client.get('/admin/model')
    assert models[0].content in response.text
    assert models[1].content in response.text
    assert models[2].content in response.text

    response = client.get('/admin/model/1')
    assert 'Model' in response.text

    response = client.delete('/admin/model/%s' % models[0].pk)
    assert response.status_code == 200

    tmpl = ModelHandler.render_form_template()
