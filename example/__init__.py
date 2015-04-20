""" Setup the application. """

import muffin


app = application = muffin.Application(
    'example',

    PLUGINS=[
        'muffin_jade',
        'muffin_admin',
        'muffin_peewee',
    ],
)


@app.register('/')
def index(request):
    return "<a href='/admin'>Admin</a>"


from example.admin import *  # noqa Register admin handlers
from example.manage import * # noqa Register commands
