# Muffin-Admin

**Muffin-Admin** mounts a [react-admin](https://marmelab.com/react-admin/) single page
application on top of [Muffin-REST](https://github.com/klen/muffin-rest) resources. A resource
that already has a REST API gets list, create, edit and delete screens without writing any
JavaScript.

[Read the documentation](https://klen.github.io/muffin-admin/) for configuration, resources,
actions and authentication.

[![Documentation](https://img.shields.io/badge/docs-read%20online-blue)](https://klen.github.io/muffin-admin/)
[![Tests Status](https://github.com/klen/muffin-admin/workflows/tests/badge.svg)](https://github.com/klen/muffin-admin/actions)
[![PyPI Version](https://img.shields.io/pypi/v/muffin-admin)](https://pypi.org/project/muffin-admin/)
[![Python Versions](https://img.shields.io/pypi/pyversions/muffin-admin)](https://pypi.org/project/muffin-admin/)

<img src="https://raw.github.com/klen/muffin-admin/develop/.github/muffin-admin.png" height="200" alt="Muffin-Admin">

## Requirements

- Python 3.11 - 3.15
- Muffin >= 3.0 and Muffin-REST >= 14.2
- Peewee (`muffin-peewee-aio`) or SQLAlchemy Core (`muffin-databases`) for a storage backend

## Install

```bash
pip install muffin-admin                # core
pip install "muffin-admin[peewee]"      # Peewee ORM
pip install "muffin-admin[sqlalchemy]"  # SQLAlchemy Core
```

## Quickstart

```python
from muffin_admin import Plugin, PWAdminHandler

admin = Plugin(app)


@admin.route
class UserResource(PWAdminHandler):
    """An admin resource for the User model."""

    class Meta(PWAdminHandler.Meta):
        model = User
        filters = "email", "is_active", "role"
        columns = "email", "is_active", "role", "created"
```

The admin is served at `/admin` and the resource API at `/admin/api`. See the
[quickstart](https://klen.github.io/muffin-admin/quickstart/) for a complete application,
including models and startup.

## Features

- List, create, edit and delete screens for [Peewee ORM](http://docs.peewee-orm.com/en/latest/)
  and [SQLAlchemy Core](https://docs.sqlalchemy.org/en/14/core/) resources
- Filtering, sorting and pagination driven by Muffin-REST
- Custom actions with forms, confirmation and file downloads
- Dashboard cards and pluggable authorization hooks
- Translations, custom CSS/JS and Material-UI icons

## Documentation

| Guide | What it answers |
| ----- | --------------- |
| [Quickstart](https://klen.github.io/muffin-admin/quickstart/) | Build a working admin from scratch |
| [Configuration](https://klen.github.io/muffin-admin/configuration/) | Plugin options, config keys, environment variables |
| [Resources](https://klen.github.io/muffin-admin/resources/) | `AdminHandler.Meta` in full |
| [Custom actions](https://klen.github.io/muffin-admin/actions/) | Buttons, forms, files, confirmation |
| [Authentication](https://klen.github.io/muffin-admin/auth/) | `check_auth`, login, storage, cookies |
| [Dashboard](https://klen.github.io/muffin-admin/dashboard/) | Cards on the start page |
| [Customization](https://klen.github.io/muffin-admin/customization/) | Translations, CSS/JS, mutation mode, frontend build |
| [API reference](https://klen.github.io/muffin-admin/api/) | Classes, options and hook signatures |
| [Development](https://klen.github.io/muffin-admin/development/) | Tests, examples, docs, release |

## Development

```bash
uv sync --all-extras --dev
uv run pytest tests     # tests
make lint               # pyrefly + ruff
make docs               # build the documentation
make example-peewee     # run the Peewee example
```

See [Development](https://klen.github.io/muffin-admin/development/) for the full workflow.

## Bug tracker and contributing

Issues and pull requests: https://github.com/klen/muffin-admin

## License

MIT.
