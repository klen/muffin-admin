"""Setup admin UI."""

from muffin import ResponseJSON
from muffin_admin import PWAdminHandler, Plugin

from . import app
from .database import User, Message


admin = Plugin(app)


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
        schema_meta = {
            'load_only': ('password',),
            'dump_only': ('created',),
        }

        columns = 'id', 'email', 'is_active', 'role', 'created'
        icon = 'People'


@admin.route
class MessageResource(PWAdminHandler):

    """Create Admin Resource for the Message model."""

    class Meta:

        """Tune the resource."""

        model = Message
        filters = 'status', 'user'

        icon = 'Message'
        references = {'user': 'user.email'}
