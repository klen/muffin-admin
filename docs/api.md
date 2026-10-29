# API reference

The public objects, as imported from `muffin_admin`. The guides explain when to use them;
this is the lookup table.

## Imports

```python
from muffin_admin import (
    AdminHandler,
    Plugin,
    PWAdminHandler,
    PWFilter,
    SAAdminHandler,
    SAFilter,
)

from muffin_admin.handler import AdminOptions
from muffin_admin.peewee import PWAdminOptions, PWSearchFilter
from muffin_admin.sqlalchemy import SAAdminOptions
from muffin_admin.types import TActionView, TRAConverter, TRAInfo, TRAInputs, TRAProps
```

Backend imports are optional: `PWAdminHandler` and `SAAdminHandler` are exported only when
`muffin-peewee-aio` or `muffin-databases` are installed.

## Plugin

```python
Plugin(app: Application | None = None, **options)
```

The Muffin plugin, registered as `app.plugins["admin"]`.

| Attribute | Meaning |
| --------- | ------- |
| `name` | `"admin"`; env prefix and app config prefix |
| `cfg` | Plugin config; see [Configuration](configuration.md) |
| `api` | `muffin_rest.API` mounted at `{prefix}/api` without OpenAPI |
| `auth` | Auth state serialized into `ra.json` |
| `handlers` | Registered `AdminHandler` subclasses, in registration order |

```python
plugin.setup(app, **options)
plugin.to_ra() -> dict
plugin.route(obj, *paths, **params) -> Callable
```

`route` accepts either a handler class (`@admin.route` on the class) or a path string
(`@admin.route("/user")` on the class). With a class it registers the handler and forwards to
`api.route`; with paths it returns a decorator. Extra `params` go to `muffin_rest.API.route`.

Authorization and dashboard callbacks:

```python
plugin.check_auth(fn) -> fn      # sets api.authorize and auth["required"]
plugin.get_identity(fn) -> fn    # mounts {prefix}/ident, sets auth["identityURL"]
plugin.login(fn) -> fn           # mounts {prefix}/login, sets auth["authorizeURL"]
plugin.dashboard(fn) -> fn       # adds the "dashboard" key to ra.json
```

All four return the function unchanged and are used as decorators. See
[Authentication](auth.md) and [Dashboard](dashboard.md).

`to_ra()` serializes the plugin state:

```python
{
    "apiUrl": "{prefix}/api",
    "auth": {...},
    "adminProps": {"title", "disableTelemetry", "mutationMode"},
    "appBarLinks": [...],
    "version": "...",
    "help": None,
    "resources": [...],
    "locales": {...},
    "dashboard": ... | None,   # only with a dashboard callback
}
```

`version` comes from the installed package metadata (`importlib.metadata.version`).

## AdminHandler

```python
class AdminHandler(RESTBase[TVResource, TVCollection]):
    meta_class = AdminOptions
    meta: AdminOptions
```

```python
async def __call__(self, request, *, method_name=None, **_) -> Response
async def log(self, request, response, action: str | None) -> None
def get_selected(self, request) -> TVCollection
```

`__call__` runs the Muffin-REST request lifecycle and then `log`. `get_selected` returns the
selected objects for bulk actions: the `ids` query values in the base class, a queryset in the
backends.

```python
@classmethod
def action(*paths, methods=None, hosts=None, icon=None, label=None, view=None,
           schema=None, **opts) -> Callable
```

Behaviour is described in [Custom actions](actions.md). The decorator stores
`__route__ = (paths, methods, hosts)` and `__action__` (the payload sent to react-admin) on the
wrapped method.

Serialization helpers:

```python
@classmethod
def to_ra(cls) -> dict                                  # one resource description
@classmethod
def to_ra_schema(cls, schema_cls, *, resource=True) -> tuple[TRAInputs, TRAInputs]
@classmethod
def to_ra_field(cls, field, source) -> TRAInfo
@classmethod
def to_ra_input(cls, field, source, *, resource=True) -> TRAInfo
@classmethod
def to_ra_filter(cls, flt) -> TRAInfo
```

`to_ra_schema` returns `(fields, inputs)`; `resource=False` is used for action schemas, where
inputs are generated without model lookups.

## AdminOptions

`AdminOptions` extends `muffin_rest.options.RESTOptions`:

```python
limit = 25
limit_max = 100
limit_total = False
icon = ""
label = ""
group = None
id = "id"
create = delete = edit = show = True
actions = ()
columns = ()
help = None
locales = None
ra_order = 0
```

`ra_fields`, `ra_inputs`, `ra_filters`, `ra_refs`, `ra_links`, `ra_list_params`,
`ra_filters_always_on` and `ra_show_params` are class-level overrides. Everything is described
in [Resources](resources.md).

## Backend handlers

```python
class PWAdminOptions(AdminOptions, PWRESTOptions):
    # adds: model, manager, model_pk, delete_recursive
    # sets: id = model_pk.name, injects a primary-key filter

class PWAdminHandler(AdminHandler[TVResource, TVCollection],
                     PWRESTHandler[TVResource, TVCollection]):
    meta_class = PWAdminOptions
```

```python
class SAAdminOptions(AdminOptions, SARESTOptions):
    # adds: table, database, table_pk
    # sets: id = table_pk.name, injects a primary-key filter

class SAAdminHandler(AdminHandler[TVResource, TVCollection],
                     SARESTHandler[TVResource, TVCollection]):
    meta_class = SAAdminOptions
```

Both override `get_selected`, `to_ra_field` and `to_ra_input` to map storage types to
react-admin widgets.

`PWSearchFilter` is a Peewee filter that applies `contains()` to the column:

```python
from muffin_admin.peewee import PWSearchFilter
```

## Filters

```python
PWFilter(name, *, field=None, schema_field=None, operator=None, **meta)
SAFilter(name, *, field=None, schema_field=None, operator=None, **meta)
```

They are Muffin-REST filters with backend operators; see
[Querying](https://klen.github.io/muffin-rest/querying/) and
[Filter reference](https://klen.github.io/muffin-rest/reference/#filters).

## Types

From `muffin_admin.types`:

| Type | Definition |
| ---- | ---------- |
| `TActionView` | `Literal["show", "edit", "list", "bulk"]` |
| `TRAProps` | `dict[str, Any]` |
| `TRAInfo` | `tuple[str, TRAProps]` — widget name and props |
| `TRAConverter` | `Callable[[Field], TRAInfo]` |
| `TRAInputs` | `tuple[tuple[str, TRAInfo], ...]` |
| `TRAReference` | `TypedDict(key, source, reference, searchKey)`, all optional |
| `TRAActionLink` | `TypedDict(label, icon, title, field, filter)`, all optional |
| `TRALinks` | `tuple[tuple[str, TRAActionLink], ...]` |

`TRAReference` describes an `ra_refs` entry; `TRAActionLink` describes an `ra_links` entry.
