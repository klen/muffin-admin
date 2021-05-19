"""Setup admin UI."""

import marshmallow as ma
from muffin import ResponseJSON
from muffin_admin import PWAdminHandler, Plugin

from . import app
from .database import User, Message


admin = Plugin(app, custom_css_url='/admin.css')


# Setup authorization
# -------------------

@admin.check_auth
async def auth(request):
    """Fake authorization method. Just checks for an auth token exists in request."""
    return request.headers.get('authorization')


@admin.get_identity
async def ident(request):
    """Get current user information."""
    pk = request.headers.get('authorization')
    user = User.select().where(User.id == pk).first()
    if user:
        return {"id": user.id, "fullName": user.email}


@admin.login
async def login(request):
    """Login a user."""
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
        filters = 'email', 'created', 'is_active', 'role'
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

        columns = 'id', 'picture', 'email', 'name', 'is_active', 'role'
        icon = 'People'

    @classmethod
    def to_ra_field(cls, field, name):
        if name == 'picture':
            return 'ImageField', {
                'source': name, 'title': name, 'sortable': False, 'className': 'user-picture'}

        return super().to_ra_field(field, name)


@admin.route
class MessageResource(PWAdminHandler):

    """Create Admin Resource for the Message model."""

    class Meta:

        """Tune the resource."""

        model = Message
        filters = 'status', 'user'

        icon = 'Message'
        references = {'user': 'user.email'}
