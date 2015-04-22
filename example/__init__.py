""" Setup the application. """

import muffin


app = application = muffin.Application(
    'example',

    PLUGINS=[
        'muffin_jade',
        'muffin_admin',
        'muffin_peewee',
    ],

    JADE_TEMPLATE_FOLDERS='example/templates',

    ADMIN_TEMPLATE_LIST='custom_list.jade'
)


@app.register('/')
def index(request):
    return "<a href='/admin'>Admin</a>"


from example.admin import *  # noqa Register admin handlers
from example.manage import * # noqa Register commands
