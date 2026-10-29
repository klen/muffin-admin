# Muffin-Admin

**Muffin-Admin** mounts a [react-admin](https://marmelab.com/react-admin/) single page
application on top of [Muffin-REST](https://klen.github.io/muffin-rest/) resources. A resource
that already has a REST API gets list, create, edit and delete screens without writing any
JavaScript.

<img src="https://raw.github.com/klen/muffin-admin/develop/.github/muffin-admin.png" alt="Muffin-Admin screenshot">

The Python side describes resources, actions and authorization in `Meta` classes; the bundled
frontend renders them. Everything the frontend needs is served from `{prefix}/ra.json`, so a
resource is a subclass and a `model`:

```python
from muffin_admin import Plugin, PWAdminHandler

admin = Plugin(app)


@admin.route
class UserResource(PWAdminHandler):
    class Meta(PWAdminHandler.Meta):
        model = User
        filters = "email", "is_active"
        columns = "email", "name", "is_active", "created"
```

## Start here

- [Quickstart](quickstart.md): from an empty project to a working admin over Peewee or
  SQLAlchemy Core.
- [Configuration](configuration.md): every plugin option, config keys and environment
  variables.
- [Resources](resources.md): `AdminHandler.Meta` in full.
- [Custom actions](actions.md): buttons, forms, confirmation and file downloads.
- [Authentication](auth.md): `check_auth`, `get_identity`, login and logout.
- [Dashboard](dashboard.md): cards on the start page.
- [Customization](customization.md): CSS, JS, translations and building the frontend.
- [API reference](api.md): classes, options and hook signatures.
- [Development](development.md): setup, tests, examples, release.

## Requirements

- Python >= 3.11 (tested on 3.11, 3.12, 3.13, 3.14 and 3.15)
- [Muffin](https://github.com/klen/muffin) >= 3.0
- [Muffin-REST](https://github.com/klen/muffin-rest) >= 14.2
- Peewee (`muffin-peewee-aio`) or SQLAlchemy Core (`muffin-databases`) for the storage
  backends

Muffin 3 keeps handler routes as `(paths, methods, hosts)` tuples and Muffin-REST 14.2
follows it; older releases are not supported.

## How the pieces fit

```
Application
├── Plugin                 /admin page, /admin/ra.json, auth routes, actions
│   ├── API                /admin/api, a Muffin-REST API without OpenAPI
│   │   ├── PWAdminHandler Peewee models
│   │   └── SAAdminHandler SQLAlchemy Core tables
│   └── dashboard          cards on the start page
└── frontend/main.js       react-admin bundle, served from the package
```

`Plugin.setup()` mounts the admin page, the `ra.json` description, the login and identity
routes, and the Muffin-REST API. Handlers registered with `@admin.route` are serialized into
`ra.json`; the frontend builds the screens from that description. See
[Resources](resources.md) and [API reference](api.md) for the details.

## Install

```bash
pip install muffin-admin                # core
pip install "muffin-admin[peewee]"      # Peewee ORM
pip install "muffin-admin[sqlalchemy]"  # SQLAlchemy Core
```

The package ships `main.js` built from `frontend/`. Without it the admin page loads but
react-admin has nothing to run; see [Customization](customization.md#building-the-frontend)
for building a bundle from a source checkout.
