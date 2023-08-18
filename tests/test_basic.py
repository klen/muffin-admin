import marshmallow as ma
from marshmallow import validate


def test_endpoint(app):
    from muffin_admin import AdminHandler, Plugin

    admin = Plugin(app)
    assert admin

    @admin.route
    class BaseHandler(AdminHandler):
        class Meta:
            name = "base"
            filters = "id", "name"
            sorting = "id", "name"

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
    assert not ra["icon"]
    assert ra["delete"] is True
    assert ra["create"] == [
        ("TextInput", {"source": "id"}),
        ("TextInput", {"source": "name"}),
        ("BooleanInput", {"source": "active", "helperText": "Is active?"}),
    ]
    assert ra["edit"] == {
        "actions": [],
        "inputs": [
            ("TextInput", {"source": "id"}),
            ("TextInput", {"source": "name"}),
            ("BooleanInput", {"source": "active", "helperText": "Is active?"}),
        ],
    }
    assert ra["show"] == {
        "actions": [],
        "links": {},
        "fields": [
            ("TextField", {"source": "id"}),
            ("TextField", {"source": "name"}),
            ("BooleanField", {"source": "active"}),
        ],
    }
    assert ra["list"] == {
        "actions": [],
        "fields": [
            ("TextField", {"source": "id", "sortable": True}),
            ("BooleanField", {"source": "active", "sortable": False}),
            ("TextField", {"source": "name", "sortable": True}),
        ],
        "filters": [("TextInput", {"source": "id"}), ("TextInput", {"source": "name"})],
        "limit": 25,
        "limitMax": 100,
        "show": True,
        "edit": True,
    }


async def test_endpoint_action(app):
    from muffin_admin import AdminHandler, Plugin

    admin = Plugin(app)
    assert admin

    @admin.route
    class Handler(AdminHandler):
        class Meta:
            name = "handler"
            filters = "id", "name"
            sorting = "id", "name"

        @AdminHandler.action("/base")
        async def base_action(self, request, response=None):
            pass

    ra = Handler.to_ra()
    assert ra["list"]["actions"] == [
        {"view": "list", "icon": None, "action": "/base", "title": None, "label": "base_action"},
    ]


def test_custom_fields_inputs():
    from muffin_admin import AdminHandler

    class BaseHandler(AdminHandler):
        class Meta:
            name = "name"
            filters = "id", "name"
            sorting = "id", "name"

            class Schema(ma.Schema):
                id = ma.fields.String()
                name = ma.fields.String(validate=validate.Length(3, 100))
                active = ma.fields.Boolean()

            columns = "id", "active", "name", "unknown"
            ra_inputs = {
                "id": "NumberInput",
            }

    ra = BaseHandler.to_ra()
    assert ra["create"] == [
        ("NumberInput", {"source": "id"}),
        ("TextInput", {"source": "name"}),
        ("BooleanInput", {"source": "active"}),
    ]


def test_schema_opts():
    from muffin_admin import AdminHandler

    class BaseHandler(AdminHandler):
        class Meta:
            name = "name"
            filters = "id", "name"
            sorting = "id", "name"

            class Schema(ma.Schema):
                id = ma.fields.String()
                name = ma.fields.String(validate=validate.Length(3, 100))
                active = ma.fields.Boolean()

                class Meta:
                    fields = "name", "id"

    ra = BaseHandler.to_ra()
    assert ra
    assert ra["edit"] == {
        "actions": [],
        "inputs": [
            ("TextInput", {"source": "name"}),
            ("TextInput", {"source": "id"}),
        ],
    }
