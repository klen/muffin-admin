import muffin


async def test_base(app, client):

    # Install plugins
    from muffin_babel import Plugin as Babel
    from muffin_jinja2 import Plugin as Jinja2

    Babel(app)
    Jinja2(app)

    # Install the admin
    from muffin_admin import Plugin as Admin

    Admin(app)

    @app.register
    class Test(admin.Handler):

        columns = 'id', 'name'

        def load_one(self, request):
            resource = request.match_info.get(self.name)
            if resource:
                return self.collection[int(resource) - 1]

        def load_many(self, request):
            return [
                muffin.utils.Struct(id=1, name='test1'),
                muffin.utils.Struct(id=2, name='test2'),
            ]

    @admin.authorization
    def ensure_code_in_get(request):
        """ Simple fake authentication process. """
        if 'auth' not in request.query:
            raise muffin.HTTPForbidden()
        return True

    client = await aiohttp_client(app)

    async with client.get('/admin') as resp:
        assert resp.status == 403

    async with client.get('/admin?auth=1') as resp:
        assert resp.status == 200

    assert admin.handlers

    th = admin.handlers['test']
    assert th.name == 'test'

    async with client.get('/admin/test?auth=1') as resp:
        assert resp.status == 200
        text = await resp.text()
        assert 'test1' in text
        assert 'test2' in text


async def test_peewee(aiohttp_client):
    app = muffin.Application('pw_admin', PEEWEE_CONNECTION='sqlite:///:memory:')
    app.install('muffin_jinja2')
    db = app.install('muffin_peewee')
    admin = app.install('muffin_admin')

    import peewee as pw
    from muffin_peewee.fields import JSONField

    @db.register
    class Child(db.TModel):
        active = pw.BooleanField()

    @db.register
    class Model(db.TModel):

        active = pw.BooleanField()
        number = pw.IntegerField(default=1, choices=zip(range(3), range(3)))
        content = pw.CharField()
        config = JSONField(default={})
        child = pw.ForeignKeyField(Child, null=True)

    @db.register
    class Model2(db.TModel):
        pass

    Child.create_table()
    Model.create_table()
    Model2.create_table()

    from muffin_admin.peewee import PWAdminHandler, PWFilter

    @app.register
    class ModelHandler(PWAdminHandler):
        model = Model
        columns_exclude = 'created',
        columns_filters = 'content', 'child.active', PWFilter('test', Model.number)
        form_exclude = 'number',

    @ModelHandler.action
    def test(handler, request):
        return 'PASSED'

    assert ModelHandler.actions
    assert ModelHandler.columns
    assert ModelHandler.columns == ['id', 'active', 'number', 'content', 'config', 'child']
    assert ModelHandler.name == 'model'
    assert ModelHandler.form
    assert ModelHandler.form.config
    assert ModelHandler.can_create
    assert ModelHandler.can_edit
    assert ModelHandler.can_delete
    assert ModelHandler.columns_formatters is not PWAdminHandler.columns_formatters

    # Make admin handler dynamically
    admin.register(Model2, can_delete=False)
    handler = admin.handlers['model2']
    assert handler.model == Model2
    assert handler.can_delete is False

    from mixer.backend.peewee import Mixer
    mixer = Mixer(commit=True)
    models = mixer.cycle(3).blend(Model, number=(n for n in (1, 2, 3)))

    client = await aiohttp_client(app)

    async with client.get('/admin/model?auth=1') as resp:
        assert resp.status == 200
        text = await resp.text()
        assert models[0].content in text
        assert models[1].content in text
        assert models[2].content in text

    async with client.get('/admin/model?pk=1&auth=1') as resp:
        assert resp.status == 200
        text = await resp.text()
        assert 'created' in text

    async with client.post('/admin/model?pk=1&auth=1', data={
            'content': 'new content'
            }) as resp:
        assert resp.status == 200

    async with client.delete('/admin/model?pk=1&auth=1'):
        assert not Model.select().where(Model.id == 1).exists()

    async with client.get('/admin/model2?auth=1') as resp:
        assert resp.status == 200

    async with client.get('/admin/model?auth=1&af-content=%s' % models[1].content) as resp:
        assert resp.status == 200
        text = await resp.text()
        assert models[1].content in text
        assert not models[2].content in text

    async with client.get('/admin/model?auth=1&af-test=%s' % models[1].number) as resp:
        assert resp.status == 200
        text = await resp.text()
        assert models[1].content in text
        assert not models[2].content in text

    async with client.get('/admin/model?auth=1&af-test=invalid') as resp:
        assert resp.status == 200
