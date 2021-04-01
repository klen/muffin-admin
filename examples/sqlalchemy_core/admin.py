from muffin_admin import SAAdminHandler, Plugin
from muffin import ResponseJSON

from . import app
from .database import User, Message, db


admin = Plugin(app)


# Setup authorization
# -------------------

@admin.check_auth
async def auth(request):
    """Fake authorization method. Just checks for an auth token exists in request."""
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
    """Login a user."""
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
        filters = 'email', 'created', 'is_active', 'role'
        schema_meta = {
            'load_only': ('password',),
            'dump_only': ('created',),
        }

        columns = 'id', 'email', 'is_active', 'role', 'created'
        icon = 'People'


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
