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
    sa.Column('meta', sa.JSON, default={}),

    sa.Column('role_id', sa.ForeignKey('role.id'), nullable=False),
)

Message = sa.Table(
    'message', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('user_id', sa.ForeignKey('user.id'), nullable=False),
)


#  @pytest.fixture(autouse=True)
#  async def setup_db(app):
#      db.setup(app)
#      #  await db.execute(sa.schema.CreateTable(Role))
#      #  await db.execute(sa.schema.CreateTable(User))
#      #  await db.execute(sa.schema.CreateTable(Message))


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

    @admin.route
    class MessageAdmin(SAAdminHandler):

        class Meta:
            table = Message
            database = db


def test_admin(app):
    admin = app.plugins['admin']
    assert admin.to_ra()

    assert admin.api.router.routes()
    assert admin.handlers


def test_admin_schemas(app):
    admin = app.plugins['admin']
    UserResource = admin.handlers[0]
    assert UserResource.meta.limit
    assert UserResource.meta.columns
    assert UserResource.meta.sorting

    ra = UserResource.to_ra()
    assert ra['name'] == 'user'
    assert ra['label'] == 'user'
    assert ra['icon'] == ''
    assert ra['delete'] is True
    assert ra['create'] == [
        ('NumberInput', {'source': 'id'}),
        ('TextInput', {'required': True, 'source': 'name'}),
        ('TextInput', {'source': 'password'}),
        ('BooleanInput', {'source': 'is_active'}),
        ('SelectInput', {
            'choices': [{'id': 1, 'name': 'new'}, {'id': 2, 'name': 'old'}],
            'source': 'status'}),
        ('JsonInput', {'source': 'meta'}),
        ('NumberInput', {'required': True, 'source': 'role_id'})
    ]
    assert ra['edit'] == {
        'actions': [],
        'inputs': [
            ('NumberInput', {'source': 'id'}),
            ('TextInput', {'required': True, 'source': 'name'}),
            ('TextInput', {'source': 'password'}),
            ('BooleanInput', {'source': 'is_active'}),
            ('SelectInput', {
                'choices': [{'id': 1, 'name': 'new'}, {'id': 2, 'name': 'old'}],
                'source': 'status'
            }),
            ('JsonInput', {'source': 'meta'}),
            ('NumberInput', {'required': True, 'source': 'role_id'})
        ]
    }
    assert ra['show'] == {
        'actions': [],
        'fields': [
            ('NumberField', {'source': 'id'}),
            ('TextField', {'source': 'name'}),
            ('BooleanField', {'source': 'is_active'}),
            ('TextField', {'source': 'status'}),
            ('BooleanField', {'source': 'is_super'}),
            ('JsonField', {'source': 'meta'}),
            ('NumberField', {'source': 'role_id'})
        ]
    }
    assert ra['list'] == {
        'actions': [],
        'perPage': 20, 'show': True, 'edit': True,
        'sort': {'field': 'id', 'order': 'DESC'},
        'children': [
            ('NumberField', {'source': 'id', 'sortable': True}),
            ('TextField', {'source': 'name', 'sortable': True}),
            ('BooleanField', {'source': 'is_active', 'sortable': True}),
            ('TextField', {'source': 'status', 'sortable': True}),
            ('BooleanField', {'source': 'is_super', 'sortable': True}),
            ('JsonField', {'source': 'meta', 'sortable': True}),
            ('NumberField', {'source': 'role_id', 'sortable': True})
        ],
        'filters': [
            ('TextInput', {'source': 'id'}),
            ('SelectInput', {'source': 'status', 'choices': [
                {'id': 1, 'name': 'new'}, {'id': 2, 'name': 'old'}]})
        ]
    }

    MessageResource = admin.handlers[2]
    assert MessageResource.to_ra()['edit'] == {
        'actions': [],
        'inputs': [
            ('TextInput', {'source': 'body', 'required': True, 'multiline': True}),
            ('NumberInput', {'source': 'user_id', 'required': True})
        ]
    }
