Muffin-Admin
############

.. _description:

Muffin-Admin -- an extension to Muffin_ that implements admin-interfaces

.. _badges:

.. image:: http://img.shields.io/travis/klen/muffin-admin.svg?style=flat-square
    :target: http://travis-ci.org/klen/muffin-admin
    :alt: Build Status

.. image:: http://img.shields.io/pypi/v/muffin-admin.svg?style=flat-square
    :target: https://pypi.python.org/pypi/muffin-admin

.. _contents:

.. contents::

.. _requirements:

Requirements
=============

- python >= 3.3

.. _installation:

Installation
=============

**Muffin-Admin** should be installed using pip: ::

    pip install muffin-admin

.. _usage:

Usage
=====

See a example application.
Enter `make run` for run.

Options
-------

========================== ==============================================================
 *ADMIN_PREFIX*             Admin's HTTP prefix (``/admin``)
 *ADMIN_NAME*               Admin's name (``<app.name.title()> admin``)
 *ADMIN_HOME*               A callable object that provides the admin's home view
 *ADMIN_I18N*               Internationalization support (``False``)
 *ADMIN_TEMPLATE_LIST*      Path to a template (``admin/list.html``)
 *ADMIN_TEMPLATE_ITEM*      Path to a template (``admin/item.html``)
 *ADMIN_TEMPLATE_HOME*      Path to a template (``admin/home.html``)
========================== ==============================================================

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
=======

Licensed under a `MIT license`_.

If you wish to express your appreciation for the project, you are welcome to send
a postcard to: ::

    Kirill Klenov
    pos. Severny 8-3
    MO, Istra, 143500
    Russia

.. _links:


.. _klen: https://github.com/klen
.. _Muffin: https://github.com/klen/muffin

.. _MIT license: http://opensource.org/licenses/MIT
