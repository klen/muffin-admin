import marshmallow as ma
from muffin_admin import Plugin, SAAdminHandler, SAFilter
from muffin import ResponseJSON

from . import app
from .database import User, Message, db


admin = Plugin(app, custom_css_url='/admin.css')


@admin.dashboard
async def dashboard(request):
    """Render dashboard cards."""
    return [
        [
            {'title': 'App config (Table view)', 'value': [(k, str(v)) for k, v in app.cfg]},
            {'title': 'Request headers (JSON view)', 'value': {
                k: v for k, v in request.headers.items() if k != 'cookie'}},
        ]
    ]


# Setup authorization
# -------------------

@admin.check_auth
async def auth(request):
    """Fake authorization method. Do not use in production."""
    pk = request.headers.get('authorization')
    qs = User.select().where(User.columns.id == pk)
    user = await db.fetch_one(qs)
    return user


@admin.get_identity
async def ident(request):
    """Get current user information."""
    user = await auth(request)
    if user:
        return {"id": user.id, "fullName": user.email}


@admin.login
async def login(request):
    """Login an user."""
    data = await request.data()
    qs = User.select().where(
        (User.columns.email == data['username']) &
        (User.columns.password == data['password'])
    )
    user = await db.fetch_one(qs)
    return ResponseJSON(user and user.id)


# Setup handlers
# --------------


@admin.route
class UserResource(SAAdminHandler):

    """Create Admin Resource for the User model."""

    class Meta:

        """Tune the resource."""

        database = db
        table = User
        filters = 'created', 'is_active', 'role', SAFilter('email', operator='$contains')
        sorting = 'id', 'created', 'email', 'is_active', 'role'
        schema_meta = {
            'load_only': ('password',),
            'dump_only': ('created',),
        }
        schema_fields = {
            'name': ma.fields.Function(
                lambda user: "{first_name} {last_name}".format(**user)
            )
        }

        icon = 'People'
        columns = 'id', 'picture', 'email', 'name', 'is_active', 'role'
        ra_fields = {
            'picture': ('AvatarField', {'alt': 'picture', 'nameProp': 'name', 'sortable': False})
        }


@admin.route
class MessageResource(SAAdminHandler):

    """Create Admin Resource for the Message model."""

    class Meta:

        """Tune the resource."""

        database = db
        table = Message
        filters = 'status', 'user_id'

        icon = 'Message'
        references = {'user_id': 'user.email'}
