---
title: 'Muffin-Admin'
---

::: {#description}
Muffin-Admin \-- an extension to
[Muffin](https://github.com/klen/muffin) that implements
admin-interfaces
:::

::: {#badges}
[![Build Status](http://img.shields.io/travis/klen/muffin-admin.svg?style=flat-square)](http://travis-ci.org/klen/muffin-admin)
:::

[![image](http://img.shields.io/pypi/v/muffin-admin.svg?style=flat-square)](https://pypi.python.org/pypi/muffin-admin)

::: {#contents}
::: {.contents}
:::
:::

Requirements
============

-   python \>= 3.3

Installation
============

**Muffin-Admin** should be installed using pip: :

    pip install muffin-admin

Usage
=====

See a example application. Enter [make run]{.title-ref} for run.

Options
-------

+-----------------------------------+-----------------------------------+
| > *ADMIN\_PREFIX*                 | > Admin\'s HTTP prefix (`/admin`) |
+-----------------------------------+-----------------------------------+
| > *ADMIN\_NAME*                   | > Admin\'s name                   |
|                                   | > (`<app.name.title()> admin`)    |
+-----------------------------------+-----------------------------------+
| > *ADMIN\_HOME*                   | > A callable object that provides |
|                                   | > the admin\'s home view          |
+-----------------------------------+-----------------------------------+
| > *ADMIN\_I18N*                   | > Internationalization support    |
|                                   | > (`False`)                       |
+-----------------------------------+-----------------------------------+
| > *ADMIN\_TEMPLATE\_LIST*         | > Path to a template              |
|                                   | > (`admin/list.html`)             |
+-----------------------------------+-----------------------------------+
| > *ADMIN\_TEMPLATE\_ITEM*         | > Path to a template              |
|                                   | > (`admin/item.html`)             |
+-----------------------------------+-----------------------------------+
| > *ADMIN\_TEMPLATE\_HOME*         | > Path to a template              |
|                                   | > (`admin/home.html`)             |
+-----------------------------------+-----------------------------------+

Bug tracker {#bugtracker}
===========

If you have any suggestions, bug reports or annoyances please report
them to the issue tracker at
<https://github.com/klen/muffin-admin/issues>

Contributing
============

Development of Muffin-Admin happens at:
<https://github.com/klen/muffin-admin>

Contributors
============

-   [klen](https://github.com/klen) (Kirill Klenov)

License
=======

Licensed under a [MIT license](http://opensource.org/licenses/MIT).
