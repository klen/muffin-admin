""" Setup the application. """

import muffin


app = application = muffin.Application(
    'example',

    PLUGINS=[
        'muffin_jinja2',
        'muffin_babel',
        'muffin_admin',
        'muffin_peewee',
    ],

    JINJA2_TEMPLATE_FOLDERS='example/templates',
    JINJA2_AUTO_RELOAD=True,

    ADMIN_TEMPLATE_LIST='custom_list.html',
    ADMIN_TEMPLATE_HOME='custom_home.html',
    ADMIN_I18N=True,
)


@app.register('/')
def index(request):
    """Index page."""
    return "<a href='/admin'>Admin</a>"


from example.admin import *  # noqa Register admin handlers
from example.manage import * # noqa Register commands
