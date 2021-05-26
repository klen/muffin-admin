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
        'storage': 'localstorage',
        'storage_name': 'muffin_admin_auth',
        'logoutURL': None,
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

    handler = admin.handlers[0]
    assert handler.meta.limit == 20
    assert handler.meta.label == 'base'
    assert handler.meta.columns == ('id', 'active', 'name', 'unknown')
    assert handler.meta.sorting == {'id': True, 'name': True}

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
        'icon': '',
        'label': 'base',
        'list': {
            'children': [
                ('TextField', {'source': 'id', 'sortable': True}),
                ('BooleanField', {'source': 'active', 'sortable': False}),
                ('TextField', {'source': 'name', 'sortable': True}),
            ],
            'filters': [('TextInput', {'source': 'id'}), ('TextInput', {'source': 'name'})],
            'perPage': 20, 'show': True, 'edit': True,
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
