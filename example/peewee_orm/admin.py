"""Setup admin UI."""

from typing import ClassVar

import marshmallow as ma
from muffin import Response, ResponseJSON
from muffin_rest import APIError

from example.peewee_orm.schemas import GreetActionSchema
from muffin_admin import Plugin, PWAdminHandler

from . import app
from .database import Group, Message, User

admin = Plugin(
    app,
    custom_css_url="/admin.css",
    help="https://fakeHelpLink.com",
    locales={
        "en": {
            "resources": {
                "user": {
                    "fields": {
                        "name": "Full Name",
                        "picture": "Avatar",
                        "is_active": "Active",
                        "role": "Role",
                    },
                    "actions": {
                        "disable": "Disable Users",
                        "greet": "Greeter",
                        "error": "Broken Action",
                    },
                },
                "group": {
                    "fields": {
                        "name": "Group Name",
                    },
                },
                "message": {
                    "fields": {
                        "status": "Status",
                        "user": "User",
                    },
                    "actions": {
                        "publish": "Publish",
                    },
                },
            },
        },
        "ru": {
            "resources": {
                "user": {
                    "name": "Пользователи",
                    "fields": {
                        "name": "Полное имя",
                        "picture": "Аватар",
                        "is_active": "Активный",
                        "role": "Роль",
                    },
                    "actions": {
                        "disable": "Отключить пользователей",
                        "greet": "Приветствие",
                        "error": "Сломанное действие",
                    },
                },
                "group": {
                    "name": "Группы",
                    "fields": {
                        "name": "Имя группы",
                    },
                },
                "message": {
                    "name": "Сообщения",
                    "fields": {
                        "status": "Статус",
                        "user": "Пользователь",
                    },
                    "actions": {
                        "publish": "Опубликовать",
                    },
                },
            },
        },
    },
)


# Setup authorization
# -------------------


@admin.check_auth
async def auth(request, redirect=True):
    """Fake authorization method. Do not use in production."""
    pk = request.headers.get("authorization") or request.query.get("t")
    return await User.select().where(User.id == pk).first()


@admin.get_identity
async def ident(request):
    """Get current user information."""
    user = await auth(request, redirect=False)
    if user:
        return {"id": user.id, "fullName": user.email}


@admin.dashboard
async def dashboard(request):
    """Render dashboard cards."""
    return [
        [
            {
                "title": "App config (Table view)",
                "value": [(k, str(v)) for k, v in app.cfg],
            },
            {
                "title": "Request headers (JSON view)",
                "value": {k: v for k, v in request.headers.items() if k != "cookie"},
            },
        ],
    ]


@admin.login
async def login(request):
    """Login an user."""
    data = await request.data()
    user = (
        await User.select()
        .where(User.email == data["username"], User.password == data["password"])
        .first()
    )
    return ResponseJSON(user and user.id)


# Setup handlers
# --------------


@admin.route
class UserResource(PWAdminHandler):
    """Create Admin Resource for the User model."""

    class Meta:
        """Tune the resource."""

        model = User
        filters = "created", "is_active", "role", ("email", {"operator": "$contains"})
        sorting = ("id", {"default": "desc"}), "created", "email", "is_active", "role"
        schema_meta: ClassVar = {
            "load_only": ("password",),
            "dump_only": ("created",),
        }
        schema_fields: ClassVar = {
            "name": ma.fields.Function(
                lambda user: f"{user.first_name} {user.last_name}",
            ),
        }

        icon = "Person"
        help = "https://fakeHelpLink.com"
        columns = "id", "picture", "email", "name", "is_active", "role"
        ra_fields = (
            ("picture", ("AvatarField", {"alt": "picture", "nameProp": "name", "sortable": False})),
        )
        ra_links = (("message", {"label": "Messages", "title": "Show user messages"}),)
        ra_refs = (("group", {"source": "name"}),)
        delete = False

    @PWAdminHandler.action("/user/error", label="Broken Action", icon="Error", view=["bulk"])
    async def just_raise_an_error(self, request, resource=None):
        """Just show an error."""
        raise APIError.BAD_REQUEST(message="The action is broken")

    @PWAdminHandler.action("/user/disable", label="Disable Users", icon="Clear", view=["bulk"])
    async def disable_users(self, request, resource=None):
        """Mark selected users as inactive."""
        import asyncio

        ids = request.query.getall("ids")
        await User.update(is_active=False).where(User.id << ids)
        await asyncio.sleep(1)
        return {"status": True, "ids": ids, "message": "Users is disabled"}

    @PWAdminHandler.action(
        "/user/greet",
        "/user/{id}/greet",
        label="Greeter",
        view=["list", "show"],
        schema=GreetActionSchema,
        help="http://fakeHelpLink.com",
    )
    async def greet(self, request, resource=None, data=None):
        """Mark selected users as inactive."""
        return {"status": True, "message": "Hello {name}".format(**data)}

    @PWAdminHandler.action(
        "/user/export", label="ra.action.export", icon="Download", view=["list"], file=True
    )
    async def export(self, request, **_):
        pass


@admin.route
class GroupResource(PWAdminHandler):
    """Create Admin Resource for the Group model."""

    class Meta:
        model = Group
        schema_meta: ClassVar = {"dump_only": ("created",)}
        icon = "People"


@admin.route
class MessageResource(PWAdminHandler):
    """Create Admin Resource for the Message model."""

    class Meta:
        """Tune the resource."""

        model = Message
        filters = "status", "user"
        schema_meta: ClassVar = {"dump_only": ("created",)}

        icon = "Message"
        ra_refs = (("user", {"source": "email"}),)
        ra_fields = (("status", ("ChipField", {})),)

    @PWAdminHandler.action(
        "/message/{id}/publish", label="Publish", icon="Publish", view="show", confirm=True
    )
    async def publish_message(self, _, resource=None):
        if resource is None:
            raise APIError.NOT_FOUND()

        resource.status = "published"
        await resource.save()

        return {"status": True, "message": "Message is published"}

    @PWAdminHandler.action(
        "/message/data.csv", label="Download CSV", icon="Download", view="list", file=True
    )
    async def csv(self, _, **__):
        """Download CSV file."""
        return Response(
            content="id,created,text,user\n"
            + "\n".join(f"{m.id},{m.created},{m.title}" for m in await Message.select()),
            content_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=messages.csv"},
        )
