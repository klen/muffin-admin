import datetime as dt

import muffin_peewee
import peewee as pw
import pytest

db = muffin_peewee.Plugin(connection="sqlite:///:memory:", manage_connections=False)


@db.register
class Role(pw.Model):
    name = pw.CharField()


@db.register
class User(pw.Model):

    name = pw.CharField()
    password = pw.CharField()
    is_active = pw.BooleanField(default=True, help_text="Disable to block the user")
    status = pw.IntegerField(default=1, choices=[(1, "new"), (2, "old")])
    meta = muffin_peewee.JSONField(default={})

    created = pw.DateTimeField(default=dt.datetime.utcnow)
    is_super = pw.BooleanField(default=True)

    role = pw.ForeignKeyField(Role, null=True)


@db.register
class Message(pw.Model):
    body = pw.TextField()
    user = pw.ForeignKeyField(Role)


@pytest.fixture(params=[pytest.param(("asyncio", {"use_uvloop": False}), id="asyncio")])
def aiolib(request):
    return request.param


@pytest.fixture(autouse=True)
async def setup_db(app):
    db.setup(app)
    async with db:
        async with db.connection():
            await db.create_tables()
            yield db
            await db.drop_tables()


@pytest.fixture
def setup_admin(app):
    from muffin_admin import Plugin, PWAdminHandler

    admin = Plugin(app)

    @admin.route
    class UserAdmin(PWAdminHandler):
        class Meta:
            model = User
            schema_meta = {
                "dump_only": ("is_super",),
                "load_only": ("password",),
                "exclude": ("created",),
            }
            references = {"role": "name"}
            filters = ("status",)

    @admin.route
    class RoleAdmin(PWAdminHandler):
        class Meta:
            model = Role

    @admin.route
    class MessageAdmin(PWAdminHandler):
        class Meta:
            model = Message


async def test_admin(app, setup_admin):
    admin = app.plugins["admin"]
    assert admin.to_ra()

    assert admin.api.router.routes()
    assert admin.handlers

    UserResource = admin.handlers[0]
    assert UserResource.meta.limit
    assert UserResource.meta.columns
    assert UserResource.meta.sorting

    assert UserResource.meta.Schema
    assert UserResource.meta.Schema._declared_fields["is_active"].load_default is True

    ra = UserResource.to_ra()
    assert ra["delete"] is True
    assert ra["icon"] == ""
    assert ra["name"] == "user"
    assert ra["label"] == "user"
    assert ra["create"] == [
        ("TextInput", {"required": True, "source": "name"}),
        ("TextInput", {"required": True, "source": "password"}),
        (
            "BooleanInput",
            {
                "defaultValue": True,
                "source": "is_active",
                "helperText": "Disable to block the user",
            },
        ),
        (
            "SelectInput",
            {
                "choices": [{"id": 1, "name": "new"}, {"id": 2, "name": "old"}],
                "defaultValue": 1,
                "source": "status",
            },
        ),
        ("JsonInput", {"source": "meta"}),
        (
            "FKInput",
            {
                "reference": "role",
                "emptyValue": None,
                "refProp": "name",
                "refSource": "id",
                "source": "role",
            },
        ),
    ]
    assert ra["edit"] == {
        "actions": [],
        "inputs": [
            ("TextInput", {"required": True, "source": "name"}),
            ("TextInput", {"required": True, "source": "password"}),
            (
                "BooleanInput",
                {
                    "defaultValue": True,
                    "source": "is_active",
                    "helperText": "Disable to block the user",
                },
            ),
            (
                "SelectInput",
                {
                    "choices": [{"id": 1, "name": "new"}, {"id": 2, "name": "old"}],
                    "defaultValue": 1,
                    "source": "status",
                },
            ),
            ("JsonInput", {"source": "meta"}),
            (
                "FKInput",
                {
                    "reference": "role",
                    "emptyValue": None,
                    "refProp": "name",
                    "refSource": "id",
                    "source": "role",
                },
            ),
        ],
    }
    assert ra["show"] == {
        "actions": [],
        "fields": [
            ("TextField", {"source": "id"}),
            ("TextField", {"source": "name"}),
            ("BooleanField", {"source": "is_active"}),
            ("NumberField", {"source": "status"}),
            ("JsonField", {"source": "meta"}),
            ("BooleanField", {"source": "is_super"}),
            (
                "FKField",
                {
                    "source": "role",
                    "refSource": "name",
                    "reference": "role",
                },
            ),
        ],
    }
    assert ra["list"]
    assert ra["list"]["actions"] == []
    assert ra["list"]["sort"] == {"field": "id", "order": "DESC"}
    assert ra["list"]["limit"] == 25
    assert ra["list"]["limitMax"] == 100
    assert ra["list"]["show"] is True
    assert ra["list"]["edit"] is True
    assert ra["list"]["filters"] == [
        ("TextInput", {"source": "id"}),
        (
            "SelectInput",
            {
                "choices": [{"id": 1, "name": "new"}, {"id": 2, "name": "old"}],
                "defaultValue": 1,
                "source": "status",
            },
        ),
    ]

    assert ra["list"]["children"] == [
        ("TextField", {"source": "id", "sortable": True}),
        ("TextField", {"source": "name", "sortable": True}),
        ("BooleanField", {"source": "is_active", "sortable": True}),
        ("NumberField", {"source": "status", "sortable": True}),
        ("JsonField", {"source": "meta", "sortable": True}),
        ("BooleanField", {"source": "is_super", "sortable": True}),
        (
            "FKField",
            {
                "source": "role",
                "refSource": "name",
                "reference": "role",
                "sortable": True,
            },
        ),
    ]

    MessageResource = admin.handlers[2]
    assert MessageResource.to_ra()["edit"] == {
        "actions": [],
        "inputs": [
            ("TextInput", {"source": "body", "required": True, "multiline": True}),
            ("TextInput", {"source": "user", "required": True}),
        ],
    }
