import marshmallow as ma


async def test_plugin(app):
    import muffin_admin

    assert app

    admin = muffin_admin.Plugin(app)
    assert admin

    data = admin.to_ra()
    assert data['apiUrl']
    assert data['auth'] == {
        'storage': 'localstorage',
        'storage_name': 'muffin_admin_auth',
        'logoutURL': None,
        'loginURL': None,
    }


async def test_static(app, client):
    import muffin_admin

    admin = muffin_admin.Plugin(app)
    assert admin

    res = await client.get('/admin')
    assert res.status_code == 200
    assert await res.text()

    from pathlib import Path

    main_js = Path(muffin_admin.__file__).parent.parent / 'muffin_admin/main.js'
    main_js.write_text('console.log(111);')

    res = await client.get('/admin/main.js')
    assert res.status_code == 200

    main_js.unlink()


def test_endpoint(app):
    from muffin_admin import AdminHandler, Plugin

    admin = Plugin(app)
    assert admin

    @admin.route
    class BaseHandler(AdminHandler):

        class Meta:

            filters = 'id', 'name'
            sorting = 'id', 'name'

            class Schema(ma.Schema):

                id = ma.fields.String()
                name = ma.fields.String(validate=ma.validate.Length(3, 100))
                active = ma.fields.Boolean()

            columns = 'id', 'active', 'name', 'unknown'

    assert admin.api.router.routes()
    assert admin.handlers

    assert BaseHandler.meta.limit == 20
    assert BaseHandler.meta.label == 'base'
    assert BaseHandler.meta.columns == ('id', 'active', 'name', 'unknown')
    assert BaseHandler.meta.sorting == {'id': True, 'name': True}

    ra = BaseHandler.to_ra()
    assert ra['name'] == 'base'
    assert ra['label'] == 'base'
    assert ra['icon'] == ''
    assert ra['delete'] is True
    assert ra['create'] == [
        ('TextInput', {'source': 'id'}),
        ('TextInput', {'source': 'name'}),
        ('BooleanInput', {'source': 'active'})
    ]
    assert ra['edit'] == {
        'actions': [],
        'inputs': [
            ('TextInput', {'source': 'id'}),
            ('TextInput', {'source': 'name'}),
            ('BooleanInput', {'source': 'active'})
        ]
    }
    assert ra['show'] == {
        'actions': [],
        'fields': [
            ('TextField', {'source': 'id'}),
            ('TextField', {'source': 'name'}),
            ('BooleanField', {'source': 'active'})
        ]

    }
    assert ra['list'] == {
        'actions': [],
        'children': [
            ('TextField', {'source': 'id', 'sortable': True}),
            ('BooleanField', {'source': 'active', 'sortable': False}),
            ('TextField', {'source': 'name', 'sortable': True}),
        ],
        'filters': [('TextInput', {'source': 'id'}), ('TextInput', {'source': 'name'})],
        'perPage': 20, 'show': True, 'edit': True,
    }


async def test_endpoint_action(app):
    from muffin_admin import AdminHandler, Plugin

    admin = Plugin(app)
    assert admin

    @admin.route
    class Handler(AdminHandler):

        class Meta:

            filters = 'id', 'name'
            sorting = 'id', 'name'

        @AdminHandler.action('/base')
        async def base_action(self, request, response=None):
            pass

    ra = Handler.to_ra()
    assert ra['list']['actions'] == [
        {'view': 'list', 'icon': None, 'action': '/base', 'title': None, 'label': 'base_action'}]


async def test_auth(app, client):
    from muffin_admin import Plugin
    from muffin_rest import APIError

    admin = Plugin(app)

    res = await client.get('/admin/login')
    assert res.status_code == 404

    res = await client.get('/admin/ident')
    assert res.status_code == 404

    # Setup fake authorization process
    # --------------------------------

    @admin.check_auth
    async def authorize(request):
        auth = request.headers.get('authorization')
        if not auth:
            raise APIError.FORBIDDEN()

        return auth

    @admin.get_identity
    async def ident(request):
        user = request.headers.get('authorization')
        return {"id": user, "fullName": f"User-{user}"}

    @admin.login
    async def login(request):
        data = await request.data()
        return data.get('username', False)

    auth = admin.to_ra()['auth']
    assert auth
    assert auth == {
        'authorizeURL': '/admin/login',
        'identityURL': '/admin/ident',
        'loginURL': None,
        'logoutURL': None,
        'required': True,
        'storage': 'localstorage',
        'storage_name': 'muffin_admin_auth'
    }

    res = await client.get('/admin/login', data={'username': 'user', 'password': 'pass'})
    assert res.status_code == 200
    assert await res.text() == 'user'

    res = await client.get('/admin/ident', headers={'authorization': 'user'})
    assert res.status_code == 200
    assert await res.json() == {"id": "user", "fullName": "User-user"}

    res = await client.get('/admin')
    assert res.status_code == 403


def test_custom_fields_inputs(app):
    from muffin_admin import AdminHandler

    class BaseHandler(AdminHandler):

        class Meta:

            filters = 'id', 'name'
            sorting = 'id', 'name'

            class Schema(ma.Schema):

                id = ma.fields.String()
                name = ma.fields.String(validate=ma.validate.Length(3, 100))
                active = ma.fields.Boolean()

            columns = 'id', 'active', 'name', 'unknown'
            ra_inputs = {
                'id': ('NumberInput', {}),
            }

    ra = BaseHandler.to_ra()
    assert ra['create'] == [
        ('NumberInput', {'source': 'id'}),
        ('TextInput', {'source': 'name'}),
        ('BooleanInput', {'source': 'active'})
    ]


async def test_dashboard(app, client):
    import muffin_admin

    admin = muffin_admin.Plugin(app)

    @admin.dashboard
    async def dashboard(request):
        """Render admin dashboard cards."""
        return [
            {'name': 'application config', 'value': {k: str(v) for k, v in app.cfg}},
            {'name': 'request headers', 'value': dict(request.headers)},
        ]

    res = await client.get('/admin')
    assert res.status_code == 200
    text = await res.text()
    assert "dashboard" in text
    assert "application config" in text
    assert "request headers" in text
