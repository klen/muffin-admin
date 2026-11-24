from typing import ClassVar

import marshmallow as ma
from marshmallow import validate
from muffin import Application

from muffin_admin import AdminHandler, Plugin


def test_endpoint(app):

    admin = Plugin(app)
    assert admin

    @admin.route
    class BaseHandler(AdminHandler):
        class Meta:  # type: ignore[]
            name = "base"
            filters = "id", "name"
            sorting = "id", "name"
            locales: ClassVar = {
                "en": {"test": "Test"},
            }

            class Schema(ma.Schema):
                id = ma.fields.String()
                name = ma.fields.String(validate=validate.Length(3, 100))
                active = ma.fields.Boolean(metadata={"description": "Is active?"})

            columns = "id", "active", "name", "unknown"

    assert admin.api.router.routes()
    assert admin.handlers

    assert BaseHandler.meta.limit == 25
    assert BaseHandler.meta.label == "base"
    assert BaseHandler.meta.columns == ("id", "active", "name", "unknown")
    assert BaseHandler.meta.sorting
    assert "id" in BaseHandler.meta.sorting.mutations
    assert "name" in BaseHandler.meta.sorting.mutations

    ra = BaseHandler.to_ra()
    assert ra["name"] == "base"
    assert ra["label"] == "base"
    assert ra["actions"] == []
    assert not ra["icon"]
    assert ra["delete"] is True
    assert ra["create"] == [
        ("TextInput", {"source": "id"}),
        ("TextInput", {"source": "name"}),
        ("BooleanInput", {"source": "active", "helperText": "Is active?"}),
    ]
    assert ra["edit"] == {
        "remove": True,
        "inputs": [
            ("TextInput", {"source": "id"}),
            ("TextInput", {"source": "name"}),
            ("BooleanInput", {"source": "active", "helperText": "Is active?"}),
        ],
    }
    assert ra["show"] == {
        "links": (),
        "inline": (),
        "edit": True,
        "fields": [
            ("TextField", {"source": "id"}),
            ("TextField", {"source": "name"}),
            ("BooleanField", {"source": "active"}),
        ],
    }
    assert ra["list"] == {
        "fields": [
            ("TextField", {"source": "id", "sortable": True}),
            ("BooleanField", {"source": "active", "sortable": False}),
            ("TextField", {"source": "name", "sortable": True}),
        ],
        "create": True,
        "filters": [("TextInput", {"source": "id"}), ("TextInput", {"source": "name"})],
        "limit": 25,
        "limitMax": 100,
        "limitTotal": False,
        "show": True,
        "edit": True,
        "remove": True,
    }

    ra = admin.to_ra()
    assert ra["locales"] == {"en": {"test": "Test"}}


def test_default_sorting(app):
    admin = Plugin(app)

    @admin.route
    class Handler(AdminHandler):
        class Meta(AdminHandler.Meta):
            name = "sorted"
            sorting = (("id", {"default": "asc"}),)

    assert Handler.to_ra()["list"]["sort"] == {"field": "id", "order": "ASC"}


def test_app_bar_and_theme(app):
    theme = {"palette": {"secondary": {"main": "#1e88e5"}}}
    admin = Plugin(app, theme=theme, app_bar_color="#1e88e5")
    ra = admin.to_ra()
    assert ra["appBarColor"] == "#1e88e5"
    assert ra["adminProps"]["theme"] == theme

    assert Plugin(Application()).to_ra()["appBarColor"] is None


async def test_endpoint_action(app):

    admin = Plugin(app)
    assert admin

    class ActionSchema(ma.Schema):
        name = ma.fields.String()

    @admin.route
    class Handler(AdminHandler):
        class Meta(AdminHandler.Meta):
            name = "handler"
            filters = "id", "name"
            sorting = "id", "name"

        @AdminHandler.action("/base", view="show", schema=ActionSchema)
        async def base_action(self, request, response=None):
            pass

    ra = Handler.to_ra()
    assert ra["actions"] == [
        {
            "view": ["show"],
            "icon": None,
            "paths": ("/base",),
            "title": None,
            "label": "Base action",
            "id": "base_action",
            "schema": [("TextInput", {"source": "name"})],
        },
    ]
    assert ra["edit"]["inputs"] == []


def test_inline_lists():

    class BaseHandler(AdminHandler):
        class Meta(AdminHandler.Meta):
            name = "base"
            ra_inline: ClassVar = (("message", {"filter": "user"}),)

            class Schema(ma.Schema):  # type: ignore[]
                id = ma.fields.String()

    assert BaseHandler.to_ra()["show"]["inline"] == (("message", {"filter": "user"}),)


def test_action_route():

    @AdminHandler.action("/base", view="show", hosts="example.com")
    async def base_action(self, request):
        pass

    assert base_action.__route__ == (("/base",), None, "example.com")  # type: ignore[]


def test_custom_fields_inputs():

    class BaseHandler(AdminHandler):
        class Meta(AdminHandler.Meta):
            name = "name"
            filters = "id", "name"
            sorting = "id", "name"

            class Schema(ma.Schema):  # type: ignore[]
                id = ma.fields.String()
                name = ma.fields.String(validate=validate.Length(3, 100))
                active = ma.fields.Boolean()

            columns = "id", "active", "name", "unknown"
            ra_inputs: ClassVar = {"id": "NumberInput"}

    ra = BaseHandler.to_ra()
    assert ra["create"] == [
        ("NumberInput", {"source": "id"}),
        ("TextInput", {"source": "name"}),
        ("BooleanInput", {"source": "active"}),
    ]


def test_schema_opts():

    class BaseHandler(AdminHandler):
        class Meta(AdminHandler.Meta):
            name = "name"
            filters = "id", "name"
            sorting = "id", "name"

            class Schema(ma.Schema):  # type: ignore[]
                id = ma.fields.String()
                name = ma.fields.String(validate=validate.Length(3, 100))
                active = ma.fields.Boolean()

                class Meta(ma.Schema.Meta):
                    fields = "name", "id"

    ra = BaseHandler.to_ra()
    assert ra
    assert ra["edit"] == {
        "remove": True,
        "inputs": [
            ("TextInput", {"source": "name"}),
            ("TextInput", {"source": "id"}),
        ],
    }


def test_disable_edit():

    class BaseHandler(AdminHandler):
        class Meta(AdminHandler.Meta):
            name = "name"
            filters = "id", "name"
            sorting = "id", "name"
            edit = False
            create = False
            delete = False

            class Schema(ma.Schema):  # type: ignore[]
                id = ma.fields.String()
                name = ma.fields.String(validate=validate.Length(3, 100))
                active = ma.fields.Boolean()

                class Meta(ma.Schema.Meta):
                    fields = "name", "id"

    ra = BaseHandler.to_ra()
    assert ra
    assert ra["edit"] is False
    assert ra["create"] is False
    assert ra["delete"] is False


def test_disable_delete():

    class BaseHandler(AdminHandler):
        class Meta(AdminHandler.Meta):
            name = "name"
            filters = "id", "name"
            sorting = "id", "name"
            delete = False

            class Schema(ma.Schema):  # type: ignore[]
                id = ma.fields.String()
                name = ma.fields.String(validate=validate.Length(3, 100))
                active = ma.fields.Boolean()

                class Meta(ma.Schema.Meta):
                    fields = "name", "id"

    ra = BaseHandler.to_ra()
    assert ra
    assert ra["delete"] is False
    assert ra["list"]["remove"] is False
    assert ra["edit"]["remove"] is False
