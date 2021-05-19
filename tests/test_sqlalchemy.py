import sqlalchemy as sa
import enum
import datetime as dt
import muffin_databases
import pytest


db = muffin_databases.Plugin(url='sqlite:///:memory:')


meta = sa.MetaData()

Role = sa.Table(
    'role', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(255), nullable=False),
)


class UserStatus(enum.Enum):
    new = 1
    old = 2


User = sa.Table(
    'user', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(255), nullable=False),
    sa.Column('password', sa.String(255), nullable=True),
    sa.Column('is_active', sa.Boolean, default=True),
    sa.Column('status', sa.Enum(UserStatus), default=UserStatus.new, nullable=False),
    sa.Column('created', sa.DateTime, default=dt.datetime.utcnow, nullable=False),
    sa.Column('is_super', sa.Boolean, default=False),

    sa.Column('role_id', sa.ForeignKey('role.id'), nullable=False),
)


@pytest.fixture(autouse=True)
async def setup_db(app):
    db.setup(app)
    await db.execute(
        "create table role ("
        "id integer primary key,"
        "name varchar(256) not null"
        ")"
    )
    await db.execute(
        "create table user ("
        "id integer primary key,"
        "name varchar(256) not null,"
        "password varchar(256) not null,"
        "is_active integer not null,"
        "status varchar(256) not null,"
        "created timestamp not null,"
        "is_super integer not null"
        ")"
    )


@pytest.fixture(autouse=True)
def setup_admin(app):
    from muffin_admin import Plugin, SAAdminHandler

    admin = Plugin(app)

    @admin.route
    class UserAdmin(SAAdminHandler):

        class Meta:
            table = User
            database = db
            schema_meta = {
                'dump_only': ('is_super',),
                'load_only': ('password',),
                'exclude': ('created',),
            }
            references = {"role": "role.name"}
            filters = 'status',

    @admin.route
    class RoleAdmin(SAAdminHandler):

        class Meta:
            table = Role
            database = db


@pytest.mark.parametrize('aiolib', [('asyncio', {'use_uvloop': False})])
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
        'is_active': True, 'role_id': True, 'status': True}

    assert UserResource.to_ra() == {
        'name': 'user',
        'label': 'user',
        'icon': '',
        'list': {
            'perPage': 50, 'show': True, 'edit': True,
            'children': [
                ('NumberField', {'source': 'id', 'sortable': True}),
                ('TextField', {'source': 'name', 'sortable': True}),
                ('BooleanField', {'source': 'is_active', 'sortable': True}),
                ('TextField', {'source': 'status', 'sortable': True}),
                ('BooleanField', {'source': 'is_super', 'sortable': True}),
                ('NumberField', {'source': 'role_id', 'sortable': True})
            ],
            'filters': [
                ('TextInput', {'source': 'id'}),
                ('SelectInput', {'source': 'status', 'choices': [
                    {'id': 1, 'name': 'new'}, {'id': 2, 'name': 'old'}]})
            ]
        },
        'show': [
            ('NumberField', {'source': 'id'}),
            ('TextField', {'source': 'name'}),
            ('BooleanField', {'source': 'is_active'}),
            ('TextField', {'source': 'status'}),
            ('BooleanField', {'source': 'is_super'}),
            ('NumberField', {'source': 'role_id'})
        ],
        'create': [
            ('NumberInput', {'source': 'id'}),
            ('TextInput', {'source': 'name', 'required': True}),
            ('TextInput', {'source': 'password'}),
            ('BooleanInput', {'source': 'is_active'}),
            ('SelectInput', {'source': 'status', 'choices': [
                {'id': 1, 'name': 'new'}, {'id': 2, 'name': 'old'}]}),
            ('NumberInput', {'source': 'role_id', 'required': True})
        ],
        'edit': [
            ('NumberInput', {'source': 'id'}),
            ('TextInput', {'source': 'name', 'required': True}),
            ('TextInput', {'source': 'password'}),
            ('BooleanInput', {'source': 'is_active'}),
            ('SelectInput', {'source': 'status', 'choices': [
                {'id': 1, 'name': 'new'}, {'id': 2, 'name': 'old'}]}),
            ('NumberInput', {'source': 'role_id', 'required': True})
        ],
        'delete': True
    }
