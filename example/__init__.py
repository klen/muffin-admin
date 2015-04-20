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

from example.admin import *  # noqa Register admin handlers
from example.manage import * # noqa Register commands
