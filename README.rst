Muffin-Admin
#############

.. _description:

**Muffin-Admin** -- an extension to Muffin_ that implements admin-interfaces

.. _badges:

.. image:: https://github.com/klen/muffin-admin/workflows/tests/badge.svg
    :target: https://github.com/klen/muffin-admin/actions
    :alt: Tests Status

.. image:: https://img.shields.io/pypi/v/muffin-admin
    :target: https://pypi.org/project/muffin-admin/
    :alt: PYPI Version

.. image:: https://img.shields.io/pypi/pyversions/muffin-admin
    :target: https://pypi.org/project/muffin-admin/
    :alt: Python Versions

----------

.. image:: https://raw.github.com/klen/muffin-admin/develop/.github/muffin-admin.png
   :height: 200px

.. _features:

Features
--------

- Support for `Peewee ORM`_, Mongo_, `SQLAlchemy Core`_ through `Muffin-Rest`_;
- Automatic filtering and sorting for items;

.. _contents:

.. contents::

.. _requirements:

Requirements
=============

- python >= 3.7

.. _installation:

Installation
=============

**Muffin-Admin** should be installed using pip: ::

    pip install muffin-admin

With `SQLAlchemy Core`_ support: ::

    pip install muffin-admin[sqlalchemy]

With `Peewee ORM`_ support: ::

    pip install muffin-admin[peewee]

.. _usage:

Usage
=====

Initialize the admin:

.. code-block:: python

   from muffin_admin import Plugin

   admin = Plugin(**options)

Initialize admin handlers (example for  `Peewee ORM`_):

.. code-block:: python

   from muffin_admin import PWAdminHandler

    @admin.route
    class UserResource(PWAdminHandler):

        """Create Admin Resource for the User model."""

        class Meta:

            """Tune the resource."""

            # Peewee Model for the admin resource
            model = User

            # Filters
            filters = 'email', 'created', 'is_active', 'role'

            # Tune serialization/deserialization schemas
            schema_meta = {
                'load_only': ('password',),
                'dump_only': ('created',),
            }

            # Columns to show
            columns = 'id', 'email', 'is_active', 'role', 'created'

            # Custom Material-UI icon
            icon = 'People'

Connect admin to an Muffin_ application:

.. code-block:: python

   admin.setup(app, **options)


Authentication
--------------

Decorate an authentication function with ``admin.check_auth``:

.. code-block:: python

    @admin.check_auth
    async def auth(request):
        """Fake authorization method. Just checks for an auth token exists in request."""
        return request.headers.get('authorization')


Register a function to return user's information:

.. code-block:: python

    @admin.get_identity
    async def ident(request):
        """Get current user information."""
        pk = request.headers.get('authorization')
        user = User.select().where(User.id == pk).first()
        if user:
            return {"id": user.id, "fullName": user.email}

Implement a login handler for standart react-admin auth page:

.. code-block:: python

    @admin.login
    async def login(request):
        """Login a user."""
        data = await request.data()
        user = User.select().where(
            User.email == data['username'], User.password == data['password']).first()
        return ResponseJSON(user and user.id)


For futher reference check `https://github.com/klen/muffin-admin/tree/develop/examples <examples>` in the repository.

Custom Actions
---------------

.. code-block:: python

   from muffin_admin import PWAdminHandler

    @admin.route
    class UserResource(PWAdminHandler):

        # ...

        @PWAdminHandler.action('users/disable', view='list')
        async def disable_users(self, request, resource=None):
            # ...

        @PWAdminHandler.action('users/{id}/admin', view='show')
        async def mark_admin(self, request, resource=None):
            # ...


Configuration options
----------------------

=========================== ==================================================== =========================== 
Name                        Default value                                        Description
--------------------------- ---------------------------------------------------- ---------------------------
**prefix**                  ``"/admin"``                                         Admin's HTTP URL prefix
**title**                   ``"Muffin Admin"``                                   Admin's title
**custom_js_url**           ``""``                                               A link to custom JS file
**custom_css_url**          ``""``                                               A link to custom CSS file
**logout_url**              ``None``                                             An HTTP URL for your custom logout page
**auth_storage**            ``"localstorage"``                                   Where to keep authorization information (localstorage|cookies)
**auth_storage_name**       ``muffin_admin_auth``                                Localstorage/Cookie name for authentication info
**app_bar_links**           ``[{'url': '/', 'icon': 'Home', 'title': 'Home'}]``  Appbar links
=========================== ==================================================== =========================== 

.. _bugtracker:

Bug tracker
===========

If you have any suggestions, bug reports or
annoyances please report them to the issue tracker
at https://github.com/klen/muffin-admin/issues

.. _contributing:

Contributing
============

Development of Muffin-Admin happens at: https://github.com/klen/muffin-admin


Contributors
=============

* klen_ (Kirill Klenov)

.. _license:

License
========

Licensed under a `MIT license`_.

.. _links:

.. _klen: https://github.com/klen
.. _Muffin: https://github.com/klen/muffin
.. _MIT license: http://opensource.org/licenses/MIT
.. _Mongo: https://www.mongodb.com/
.. _Peewee ORM: http://docs.peewee-orm.com/en/latest/
.. _SqlAlchemy Core: https://docs.sqlalchemy.org/en/14/core/
.. _Muffin-Rest: https://github.com/klen/muffin-rest
