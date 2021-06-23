"""Setup admin UI."""

import marshmallow as ma
from muffin import ResponseJSON
from muffin_rest import APIError
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
        ra_fields = {
            'picture': ('AvatarField', {
                'alt': 'picture', 'nameProp': 'name', 'sortable': False
            })
        }

    @PWAdminHandler.action('/user/error', label='Broken Action', icon='Error')
    async def just_raise_an_error(self, request, resource=None):
        """Just show an error."""
        raise APIError.BAD_REQUEST(message='The action is broken')

    @PWAdminHandler.action('/user/disable', label='Disable Users', icon='Clear')
    async def disable_users(self, request, resource=None):
        """Mark selected users as inactive."""
        import asyncio

        ids = request.query.getall('ids')
        User.update(is_active=False).where(User.id << ids).execute()
        await asyncio.sleep(1)
        return {'status': True, 'ids': ids, 'message': 'Users is disabled'}


@admin.route
class MessageResource(PWAdminHandler):

    """Create Admin Resource for the Message model."""

    class Meta:

        """Tune the resource."""

        model = Message
        filters = 'status', 'user'

        icon = 'Message'
        references = {'user': 'user.email'}

    @PWAdminHandler.action('/message/{id}/publish', label='Publish', icon='Publish', view='show')
    async def publish_message(self, request, resource=None):
        if resource is None:
            raise APIError.NOT_FOUND()

        resource.status = 'published'
        resource.save()

        return {'status': True, 'message': 'Message is published'}
