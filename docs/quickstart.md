# Quickstart

This page builds a small admin for a Peewee model and then shows the same handler over
SQLAlchemy Core. The full applications live in `example/peewee_orm/` and
`example/sqlalchemy_core/` in the repository.

## Install

```bash
pip install "muffin-admin[peewee]" uvicorn
```

## Define the application

```python title="app.py"
import datetime as dt
from pathlib import Path

from muffin import Application
from muffin_peewee import Plugin as Peewee
from peewee_aio import AIOModel, fields

from muffin_admin import Plugin, PWAdminHandler

app = Application("shop", debug=True)
db = Peewee(app, connection=f"sqlite:///{Path(__file__).parent / 'shop.sqlite'}")


class BaseModel(AIOModel):
    created = fields.DateTimeField(default=dt.datetime.utcnow)


@db.register
class User(BaseModel):
    email = fields.CharField(primary_key=True)
    name = fields.CharField()
    is_active = fields.BooleanField(default=True)


admin = Plugin(app)


@admin.route
class UserResource(PWAdminHandler):
    class Meta(PWAdminHandler.Meta):
        model = User
        filters = "email", "is_active"
        columns = "email", "name", "is_active", "created"
        icon = "People"


@app.on_startup
async def start():
    async with db:
        await db.create_tables()
```

`Plugin(app)` registers `/admin` and its API under `/admin/api`. `@admin.route` needs a
handler class and reads the model from `Meta`. The admin then exposes list, create, edit and
delete screens for it.

## Run

```bash
uvicorn app:app --reload
```

Open <http://127.0.0.1:8000/admin>. Without an authorization callback the admin is open to
anyone; see [Authentication](auth.md) before deploying it. The page and the bundle come from the
package; [Custom frontend](frontend.md) covers replacing them.

The routes registered by the plugin are:

| Path              | Purpose                                          |
| ----------------- | ------------------------------------------------ |
| `{prefix}`        | The admin page                                   |
| `{prefix}/ra.json`| Resource description for react-admin             |
| `{prefix}/main.js`| The bundled frontend                             |
| `{prefix}/login`  | Login route, answers `404` until `@admin.login`  |
| `{prefix}/ident`  | Identity route, answers `404` until `@admin.get_identity` |
| `{prefix}/api/...`| Muffin-REST API for the registered resources     |

## What `Meta` did

- `model` is the Peewee model; the resource name and primary key come from it.
- `filters` lists the fields shown in the list filter bar. The primary key filter is added
  automatically.
- `columns` lists the list-view columns. Without it every serialized field is used.
- `icon` is a Material-UI icon name for the menu.

Sorting, pagination limits, schemas and react-admin overrides are described in
[Resources](resources.md). Buttons on the resource are described in [Custom actions](actions.md).

## SQLAlchemy Core

The same plugin works with a `sqlalchemy.Table` and `muffin_databases`:

```python
import sqlalchemy as sa
from muffin_databases import Plugin as Databases

from muffin_admin import Plugin, SAAdminHandler

db = Databases(app, url="sqlite:///shop.sqlite")
meta = sa.MetaData()

User = sa.Table(
    "user",
    meta,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("email", sa.String(255), nullable=False),
    sa.Column("name", sa.String(255)),
    sa.Column("is_active", sa.Boolean, default=True),
)

admin = Plugin(app)


@admin.route
class UserResource(SAAdminHandler):
    class Meta(SAAdminHandler.Meta):
        database = db
        table = User
        filters = "email", "is_active"
        columns = "id", "email", "name", "is_active"
```

`database` and `table` are both required. Tables are not created by the admin; use your
migration tool or `sa.MetaData.create_all()` with the matching engine. The repository example
runs against the SQLite file the Peewee example creates:

```bash
make example-peewee    # creates example/db.sqlite and serves the Peewee admin
make example-sqlalchemy
```

Neither backend is mandatory: `muffin_admin` imports `PWAdminHandler` and `SAAdminHandler`
only when `muffin-peewee-aio` or `muffin-databases` are installed.
