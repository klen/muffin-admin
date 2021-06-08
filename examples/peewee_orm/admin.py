"""Setup admin UI."""

import marshmallow as ma
from muffin import ResponseJSON
from muffin_admin import Plugin, PWAdminHandler, PWFilter

from . import app
from .database import User, Message


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
async def auth(request, redirect=True):
    """Fake authorization method. Do not use in production."""
    pk = request.headers.get('authorization')
    return User.select().where(User.id == pk).first()


@admin.get_identity
async def ident(request):
    """Get current user information."""
    user = await auth(request, redirect=False)
    if user:
        return {"id": user.id, "fullName": user.email}


@admin.login
async def login(request):
    """Login an user."""
    data = await request.data()
    user = User.select().where(
        User.email == data['username'], User.password == data['password']).first()
    return ResponseJSON(user and user.id)


# Setup handlers
# --------------


@admin.route
class UserResource(PWAdminHandler):

    """Create Admin Resource for the User model."""

    class Meta:

        """Tune the resource."""

        model = User
        filters = 'created', 'is_active', 'role', PWFilter('email', operator='$contains')
        sorting = 'id', 'created', 'email', 'is_active', 'role'
        schema_meta = {
            'load_only': ('password',),
            'dump_only': ('created',),
        }
        schema_fields = {
            'name': ma.fields.Function(
                lambda user: f"{user.first_name} {user.last_name}"
            )
        }

        icon = 'People'
        columns = 'id', 'picture', 'email', 'name', 'is_active', 'role'
        ra_fields = {'picture': (
            'ImageField', {'title': 'picture', 'sortable': False, 'className': 'user-picture'}
        )}


@admin.route
class MessageResource(PWAdminHandler):

    """Create Admin Resource for the Message model."""

    class Meta:

        """Tune the resource."""

        model = Message
        filters = 'status', 'user'

        icon = 'Message'
        references = {'user': 'user.email'}
