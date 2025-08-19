import datetime as dt
import enum
from typing import ClassVar

import muffin_databases
import pytest
import sqlalchemy as sa

db = muffin_databases.Plugin(url="sqlite:///:memory:")


meta = sa.MetaData()

Role = sa.Table(
    "role",
    meta,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(255), nullable=False),
)


class UserStatus(enum.Enum):
    new = 1
    old = 2


User = sa.Table(
    "user",
    meta,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(255), nullable=False),
    sa.Column("password", sa.String(255), nullable=True),
    sa.Column("is_active", sa.Boolean, default=True),
    sa.Column("status", sa.Enum(UserStatus), default=UserStatus.new, nullable=False),
    sa.Column("created", sa.DateTime, default=dt.datetime.utcnow, nullable=False),
    sa.Column("is_super", sa.Boolean, default=False),
    sa.Column("meta", sa.JSON, default={}),
    sa.Column("role_id", sa.ForeignKey("role.id"), nullable=False),
)

Message = sa.Table(
    "message",
    meta,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("body", sa.Text(), nullable=False),
    sa.Column("user_id", sa.ForeignKey("user.id"), nullable=False),
)


#  @pytest.fixture(autouse=True)
#  async def setup_db(app):


@pytest.fixture(autouse=True)
def setup_admin(app):
    from muffin_admin import Plugin, SAAdminHandler

    admin = Plugin(app)

    @admin.route
    class UserAdmin(SAAdminHandler):
        class Meta(SAAdminHandler.Meta):
            table = User
            database = db
            schema_meta: ClassVar = {
                "dump_only": ("is_super",),
                "load_only": ("password",),
                "exclude": ("created",),
            }
            filters = ("status",)
            ra_refs: ClassVar = {"role_id": {"source": "name"}}

    @admin.route
    class RoleAdmin(SAAdminHandler):
        class Meta(SAAdminHandler.Meta):
            table = Role
            database = db

    @admin.route
    class MessageAdmin(SAAdminHandler):
        class Meta(SAAdminHandler.Meta):
            table = Message
            database = db
            ra_refs: ClassVar = {"user_id": {"source": "email"}}


def test_admin(app):
    admin = app.plugins["admin"]
    assert admin.to_ra()

    assert admin.api.router.routes()
    assert admin.handlers


def test_admin_schemas(app):
    admin = app.plugins["admin"]
    UserResource = admin.handlers[0]
    assert UserResource.meta.limit
    assert UserResource.meta.columns
    assert UserResource.meta.sorting

    ra = UserResource.to_ra()
    assert ra["name"] == "user"
    assert ra["label"] == "user"
    assert ra["icon"] == ""
    assert ra["delete"] is True
    assert ra["create"] == [
        ("NumberInput", {"source": "id"}),
        ("TextInput", {"required": True, "source": "name"}),
        ("TextInput", {"source": "password"}),
        ("BooleanInput", {"source": "is_active"}),
        (
            "SelectInput",
            {
                "choices": [{"id": 1, "name": "new"}, {"id": 2, "name": "old"}],
                "source": "status",
            },
        ),
        ("JsonInput", {"source": "meta"}),
        (
            "FKInput",
            {
                "required": True,
                "reference": "role",
                "emptyValue": "",
                "refSource": "name",
                "refKey": "id",
                "source": "role_id",
            },
        ),
    ]
    assert ra["edit"] == {
        "remove": True,
        "inputs": [
            ("NumberInput", {"source": "id"}),
            ("TextInput", {"required": True, "source": "name"}),
            ("TextInput", {"source": "password"}),
            ("BooleanInput", {"source": "is_active"}),
            (
                "SelectInput",
                {
                    "choices": [{"id": 1, "name": "new"}, {"id": 2, "name": "old"}],
                    "source": "status",
                },
            ),
            ("JsonInput", {"source": "meta"}),
            (
                "FKInput",
                {
                    "required": True,
                    "reference": "role",
                    "emptyValue": "",
                    "refSource": "name",
                    "refKey": "id",
                    "source": "role_id",
                },
            ),
        ],
    }
    assert ra["show"] == {
        "edit": True,
        "links": (),
        "fields": [
            ("NumberField", {"source": "id"}),
            ("TextField", {"source": "name"}),
            ("BooleanField", {"source": "is_active"}),
            (
                "SelectField",
                {
                    "source": "status",
                    "choices": [{"id": 1, "name": "new"}, {"id": 2, "name": "old"}],
                },
            ),
            ("BooleanField", {"source": "is_super"}),
            ("JsonField", {"source": "meta"}),
            (
                "FKField",
                {
                    "source": "role_id",
                    "refSource": "name",
                    "refKey": "id",
                    "reference": "role",
                },
            ),
        ],
    }

    assert ra["list"]
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
                "source": "status",
                "choices": [{"id": 1, "name": "new"}, {"id": 2, "name": "old"}],
            },
        ),
    ]
    assert ra["list"]["fields"] == [
        ("NumberField", {"source": "id", "sortable": True}),
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
        ("BooleanField", {"source": "is_super", "sortable": True}),
        ("JsonField", {"source": "meta", "sortable": True}),
        (
            "FKField",
            {
                "source": "role_id",
                "refSource": "name",
                "refKey": "id",
                "reference": "role",
                "sortable": True,
            },
        ),
    ]


def test_admin_schemas2(app):
    admin = app.plugins["admin"]
    MessageResource = admin.handlers[2]
    assert MessageResource.to_ra()["edit"] == {
        "remove": True,
        "inputs": [
            ("TextInput", {"source": "body", "required": True, "multiline": True}),
            (
                "FKInput",
                {
                    "required": True,
                    "reference": "user",
                    "emptyValue": "",
                    "refSource": "email",
                    "refKey": "id",
                    "source": "user_id",
                },
            ),
        ],
    }
