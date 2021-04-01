import marshmallow as ma
import json


async def test_plugin(app):
    import muffin_admin

    assert app

    admin = muffin_admin.Plugin(app)
    assert admin.json

    data = json.loads(admin.json)
    assert data['apiUrl']
    assert data['auth'] == {
        'redirectURL': None,
        'storage': 'localstorage',
        'storage_name': 'muffin_admin_auth',
    }


async def test_static(app, client):
    import muffin_admin

    admin = muffin_admin.Plugin(app)
    assert admin

    res = await client.get('/admin')
    assert res.status_code == 200
    assert await res.text()

    res = await client.get('/admin/main.js')
    assert res.status_code == 200


def test_endpoint(app):
    from muffin_admin import AdminHandler, Plugin

    admin = Plugin(app)
    assert admin

    @admin.route
    class BaseHandler(AdminHandler):

        class Meta:

            filters = 'id', 'name'

            class Schema(ma.Schema):

                id = ma.fields.String()
                name = ma.fields.String(validate=ma.validate.Length(3, 100))
                active = ma.fields.Boolean()

    assert admin.api.router.routes()
    assert admin.handlers

    handler = admin.handlers[0]
    assert handler.meta.limit == 50
    assert handler.meta.label == 'base'
    assert handler.meta.columns == ['id', 'name', 'active']
    assert handler.meta.sorting == {'id': True, 'name': True, 'active': True}

    assert handler.to_ra() == {
        'create': [
            ('TextInput', {'source': 'id'}),
            ('TextInput', {'source': 'name'}),
            ('BooleanInput', {'source': 'active'})
        ],
        'delete': True,
        'edit': [
            ('TextInput', {'source': 'id'}),
            ('TextInput', {'source': 'name'}),
            ('BooleanInput', {'source': 'active'})
        ],
        'icon': None,
        'label': 'base',
        'list': {
            'children': [
                ('TextField', {'source': 'id'}),
                ('TextField', {'source': 'name'}),
                ('BooleanField', {'source': 'active'})
            ],
            'filters': [('TextInput', {'source': 'id'}), ('TextInput', {'source': 'name'})],
            'perPage': 50
        },
        'name': 'base',
        'show': [
            ('TextField', {'source': 'id'}),
            ('TextField', {'source': 'name'}),
            ('BooleanField', {'source': 'active'})
        ]
    }


async def test_auth(app, client):
    from muffin_admin import Plugin

    admin = Plugin(app)

    res = await client.get('/admin/login')
    assert res.status_code == 404

    res = await client.get('/admin/ident')
    assert res.status_code == 404

    # Setup fake authorization process
    # --------------------------------

    @admin.check_auth
    async def auth(request):
        return request.headers.get('authorization')

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
        'identityURL': '/admin/ident',
        'loginURL': '/admin/login',
        'redirectURL': None,
        'required': True,
        'storage': 'localstorage',
        'storage_name': 'muffin_admin_auth'
    }

    res = await client.get('/admin/login', data={'username': 'user', 'password': 'pass'})
    assert res.status_code == 200
    assert await res.text() == 'user'

    res = await client.get('/admin/ident', headers={'authorization': 'user'})
    assert res.status_code == 200
    assert await res.json()
