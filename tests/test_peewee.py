import datetime as dt
from typing import ClassVar

import muffin_peewee
import peewee as pw
import pytest
from marshmallow import fields

db = muffin_peewee.Plugin(
    connection="sqlite:///:memory:", manage_connections=False, auto_connection=False
)


@db.register
class Role(pw.Model):
    name = pw.CharField()


@db.register
class User(pw.Model):
    name = pw.CharField()
    password = pw.CharField()
    is_active = pw.BooleanField(default=True, help_text="Disable to block the user")
    status = pw.IntegerField(default=1, choices=[(1, "new"), (2, "old")])
    meta: muffin_peewee.JSONLikeField = muffin_peewee.JSONLikeField(default={})

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
    async with db, db.connection():
        await db.create_tables()
        yield db
        await db.drop_tables()


@pytest.fixture(autouse=True)
def admin(app):
    from muffin_admin import Plugin, PWAdminHandler

    admin = Plugin(app)

    @admin.route
    class UserAdmin(PWAdminHandler):
        class Meta(PWAdminHandler.Meta):
            model = User
            schema_meta: ClassVar = {
                "dump_only": ("is_super",),
                "load_only": ("password",),
                "exclude": ("created",),
            }
            schema_fields: ClassVar = {
                "name": fields.String(metadata={"description": "User name"}),
            }
            ra_refs: ClassVar = {"role": {"source": "name"}}
            filters = ("status",)

    @admin.route
    class RoleAdmin(PWAdminHandler):
        class Meta(PWAdminHandler.Meta):
            model = Role

    @admin.route
    class MessageAdmin(PWAdminHandler):
        class Meta(PWAdminHandler.Meta):
            model = Message
            ra_refs: ClassVar = {"user": {"source": "email"}}

    return admin


async def test_admin(app):
    admin = app.plugins["admin"]
    assert admin.to_ra()

    assert admin.api.router.routes()
    assert admin.handlers


async def test_user_resource(app):
    admin = app.plugins["admin"]

    user_resource_type = admin.handlers[0]
    assert user_resource_type.meta.limit
    assert user_resource_type.meta.columns
    assert user_resource_type.meta.sorting

    assert user_resource_type.meta.Schema
    assert user_resource_type.meta.Schema._declared_fields["is_active"].load_default is True

    ra = user_resource_type.to_ra()
    assert ra["delete"] is True
    assert not ra["icon"]
    assert ra["name"] == "user"
    assert ra["label"] == "user"
    assert ra["create"] == [
        ("TextInput", {"helperText": "User name", "source": "name"}),
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
                "source": "role",
                "reference": "role",
                "refKey": "id",
                "refSource": "name",
            },
        ),
    ]
    assert ra["edit"] == {
        "remove": True,
        "inputs": [
            ("TextInput", {"helperText": "User name", "source": "name"}),
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
                    "source": "role",
                    "reference": "role",
                    "refKey": "id",
                    "refSource": "name",
                },
            ),
        ],
    }
    assert ra["show"] == {
        "links": (),
        "edit": True,
        "fields": [
            ("TextField", {"source": "id"}),
            ("TextField", {"source": "name"}),
            ("BooleanField", {"source": "is_active"}),
            (
                "SelectField",
                {
                    "source": "status",
                    "choices": [{"id": 1, "name": "new"}, {"id": 2, "name": "old"}],
                },
            ),
            ("JsonField", {"source": "meta"}),
            ("BooleanField", {"source": "is_super"}),
            (
                "FKField",
                {
                    "source": "role",
                    "refSource": "name",
                    "refKey": "id",
                    "reference": "role",
                },
            ),
        ],
    }
    assert ra["list"]
    assert ra["list"]["create"]
    assert ra["list"]["sort"] == {"field": "id", "order": "DESC"}
    assert ra["list"]["limit"] == 25
    assert ra["list"]["limitMax"] == 100
    assert ra["list"]["limitTotal"] is False
    assert ra["list"]["show"] is True
    assert ra["list"]["edit"] is True
    assert ra["list"]["filters"] == [
        ("TextInput", {"source": "id"}),
        (
            "SelectArrayInput",
            {
                "choices": [{"id": 1, "name": "new"}, {"id": 2, "name": "old"}],
                "source": "status",
            },
        ),
    ]

    assert ra["list"]["fields"] == [
        ("TextField", {"source": "id", "sortable": True}),
        ("TextField", {"source": "name", "sortable": True}),
        ("BooleanField", {"source": "is_active", "sortable": True}),
        (
            "SelectField",
            {
                "source": "status",
                "sortable": True,
                "choices": [{"id": 1, "name": "new"}, {"id": 2, "name": "old"}],
            },
        ),
        ("JsonField", {"source": "meta", "sortable": True}),
        ("BooleanField", {"source": "is_super", "sortable": True}),
        (
            "FKField",
            {
                "source": "role",
                "refSource": "name",
                "refKey": "id",
                "reference": "role",
                "sortable": True,
            },
        ),
    ]


async def test_msg_resource(app):
    admin = app.plugins["admin"]

    message_resource_type = admin.handlers[2]
    ra = message_resource_type.to_ra()
    assert ra["edit"] == {
        "remove": True,
        "inputs": [
            ("TextInput", {"source": "body", "required": True, "multiline": True}),
            (
                "FKInput",
                {
                    "source": "user",
                    "required": True,
                    "refSource": "email",
                    "refKey": "id",
                    "reference": "role",
                },
            ),
        ],
    }


async def test_client(client, admin, setup_db):
    response = await client.get(admin.api.prefix + "/user")
    assert response.status_code == 200
