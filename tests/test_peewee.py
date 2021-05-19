import pytest
import peewee as pw
import datetime as dt

import muffin_peewee


db = muffin_peewee.Plugin(connection='sqlite:///:memory:', manage_connections=False)


@db.register
class Role(pw.Model):
    name = pw.CharField()


@db.register
class User(pw.Model):

    name = pw.CharField()
    password = pw.CharField()
    is_active = pw.BooleanField(default=True)
    status = pw.IntegerField(default=1, choices=[(1, 'new'), (2, 'old')])

    created = pw.DateTimeField(default=dt.datetime.utcnow)
    is_super = pw.BooleanField(default=True)

    role = pw.ForeignKeyField(Role, null=True)


@pytest.fixture(autouse=True)
def setup_db(app):
    db.setup(app)

    User.create_table()
    Role.create_table()


@pytest.fixture(autouse=True)
def setup_admin(app):
    from muffin_admin import Plugin, PWAdminHandler

    admin = Plugin(app)

    @admin.route
    class UserAdmin(PWAdminHandler):

        class Meta:
            model = User
            schema_meta = {
                'dump_only': ('is_super',),
                'load_only': ('password',),
                'exclude': ('created',),
            }
            references = {"role": "role.name"}
            filters = 'status',

    @admin.route
    class RoleAdmin(PWAdminHandler):

        class Meta:
            model = Role


async def test_admin(app):
    admin = app.plugins['admin']
    assert admin.to_ra()

    assert admin.api.router.routes()
    assert admin.handlers

    UserResource = admin.handlers[0]
    assert UserResource.meta.limit
    assert UserResource.meta.columns
    assert UserResource.meta.sorting
    assert UserResource.meta.sorting == {
        'id': True, 'name': True, 'is_super': True,
        'is_active': True, 'role': True, 'status': True}

    assert UserResource.to_ra() == {
        'create': [
            ('TextInput', {'required': True, 'source': 'name'}),
            ('TextInput', {'required': True, 'source': 'password'}),
            ('BooleanInput', {'initialValue': True, 'source': 'is_active'}),
            ('SelectInput', {
                'choices': [{'id': 1, 'name': 'new'}, {'id': 2, 'name': 'old'}],
                'initialValue': 1,
                'source': 'status'}),
            ('TextInput', {'source': 'role'})
        ],
        'delete': True,
        'edit': [
            ('TextInput', {'required': True, 'source': 'name'}),
            ('TextInput', {'required': True, 'source': 'password'}),
            ('BooleanInput', {'initialValue': True, 'source': 'is_active'}),
            ('SelectInput', {
                'choices': [{'id': 1, 'name': 'new'}, {'id': 2, 'name': 'old'}],
                'initialValue': 1,
                'source': 'status'}),
            ('TextInput', {'source': 'role'})
        ],
        'icon': '',
        'label': 'user',
        'list': {
            'children': [
                ('TextField', {'source': 'id', 'sortable': True}),
                ('TextField', {'source': 'name', 'sortable': True}),
                ('BooleanField', {'source': 'is_active', 'sortable': True}),
                ('NumberField', {'source': 'status', 'sortable': True}),
                ('BooleanField', {'source': 'is_super', 'sortable': True}),
                ('ReferenceField', {
                    'link': 'show',
                    'source': 'role',
                    'sortable': True,
                    'reference': 'role',
                    'children': [('TextField', {'source': 'name'})]
                })
            ],
            'filters': [
                ('TextInput', {'source': 'id'}),
                ('SelectInput', {
                    'choices': [{'id': 1, 'name': 'new'}, {'id': 2, 'name': 'old'}],
                    'initialValue': 1,
                    'source': 'status'})
            ],
            'perPage': 50, 'show': True, 'edit': True,
        },
        'name': 'user',
        'show': [
            ('TextField', {'source': 'id'}),
            ('TextField', {'source': 'name'}),
            ('BooleanField', {'source': 'is_active'}),
            ('NumberField', {'source': 'status'}),
            ('BooleanField', {'source': 'is_super'}),
            ('ReferenceField', {
                'link': 'show',
                'source': 'role',
                'reference': 'role',
                'children': [('TextField', {'source': 'name'})]
            }),
        ]
    }
