import datetime as dt
from enum import Enum
from typing import ClassVar

import muffin_peewee
import peewee as pw
import pytest
from marshmallow import fields
from muffin_peewee import StrEnumField
from muffin_rest.peewee.schemas import CompositePKField

from muffin_admin import Plugin, PWAdminHandler

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
    meta = muffin_peewee.JSONLikeField(default={})

    created = pw.DateTimeField(default=dt.datetime.now)
    is_super = pw.BooleanField(default=True)

    role = pw.ForeignKeyField(Role, null=True)


@db.register
class Message(pw.Model):
    body = pw.TextField()
    user = pw.ForeignKeyField(User)


class OrderSource(Enum):
    WEB = "web"
    MOBILE = "mobile"
    API = "api"


@db.register
class Order(pw.Model):
    source = StrEnumField(OrderSource, default=OrderSource.WEB)
    source_id = pw.CharField()

    amount = pw.IntegerField()
    currency = pw.CharField()

    class Meta:
        primary_key = pw.CompositeKey("source", "source_id")


@pytest.fixture(params=[pytest.param(("asyncio", {"loop_factory": None}), id="asyncio")])
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

    @admin.route
    class OrderAdmin(PWAdminHandler):
        class Meta(PWAdminHandler.Meta):
            model = Order

    return admin


async def test_admin(app):
    admin = app.plugins["admin"]
    schema = admin.to_ra()
    assert schema
    assert schema["apiUrl"]
    assert schema["auth"]
    assert schema["adminProps"]
    assert schema["appBarLinks"]
    assert schema["version"]
    assert "help" in schema
    assert "locales" in schema

    assert schema["resources"]
    resources = {res["name"]: res for res in schema["resources"]}
    assert "user" in resources
    assert "role" in resources
    assert "message" in resources
    assert "order" in resources

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
                    "reference": "user",
                },
            ),
        ],
    }


async def test_order_resource_composite_key(app):
    admin = app.plugins["admin"]

    order_resource_type = admin.handlers[3]
    id_field = order_resource_type.meta.Schema._declared_fields["id"]
    assert isinstance(id_field, CompositePKField)
    assert id_field.dump_only is True

    ra = order_resource_type.to_ra()
    assert all(input_props[1]["source"] != "id" for input_props in ra["create"])
    assert ("TextField", {"source": "id"}) in ra["show"]["fields"]


async def test_order_resource_by_composite_invalid_key(client, admin, setup_db):
    res = await client.get(admin.api.prefix + "/order/web")
    assert res.status_code == 400


async def test_order_resource_by_composite_key(client, admin, setup_db):
    order = await db.manager.create(Order, source_id="42", amount=100, currency="USD")
    assert order

    response = await client.get(admin.api.prefix + "/order")
    assert response.status_code == 200
    payload = await response.json()

    response = await client.get(admin.api.prefix + "/order/web::42")
    assert response.status_code == 200

    payload = await response.json()
    resource = payload.get("data", payload)
    assert resource["id"] == "web::42"
    assert resource["source"] == "web"
    assert resource["source_id"] == "42"


async def test_message_request(client, admin, setup_db):
    user_password = str(id(client))
    user = await db.manager.create(User, name="John", password=user_password)
    message = await db.manager.create(Message, body="hello", user=user)
    message_id = message.id  # type: ignore[attr-defined]

    response = await client.get(admin.api.prefix + "/message")
    assert response.status_code == 200

    resource_response = await client.get(admin.api.prefix + f"/message/{message_id}")
    assert resource_response.status_code == 200

    payload = await resource_response.json()
    resource = payload.get("data", payload)
    assert resource["id"] == str(message_id)
    assert resource["body"] == "hello"


async def test_client(client, admin, setup_db):
    response = await client.get(admin.api.prefix + "/user")
    assert response.status_code == 200
