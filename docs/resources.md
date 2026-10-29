# Resources

A resource is an `AdminHandler` subclass whose `Meta` describes one REST collection. The
plugin turns it into a menu entry, list/create/edit/show screens, and a Muffin-REST route.

```python
from muffin_admin import PWAdminHandler


@admin.route
class UserResource(PWAdminHandler):
    class Meta(PWAdminHandler.Meta):
        model = User
        filters = "email", "is_active", "role"
        sorting = ("email", {"default": "desc"}), "created"
        columns = "email", "picture", "name", "is_active", "role"
        icon = "People"
        group = "People"
```

Always inherit from the backend `Meta` (`PWAdminHandler.Meta`, `SAAdminHandler.Meta`) and then
from `AdminHandler.Meta`: the backend `Meta` supplies `schema_base`, and `AdminOptions` copies
every non-underscore attribute from the class MRO.

## Handler classes

| Class | Requires | `Meta` key |
| ----- | -------- | ---------- |
| `AdminHandler` | nothing beyond Muffin-REST | your own schema and hooks |
| `PWAdminHandler` | `muffin-peewee-aio` | `model` |
| `SAAdminHandler` | `muffin-databases`, SQLAlchemy | `table`, `database` |

`AdminHandler` cannot load or save anything by itself: implement the Muffin-REST hooks
(`prepare_collection`, `prepare_resource`, `paginate`, `save`, `remove`) as described in the
[Muffin-REST documentation](https://klen.github.io/muffin-rest/handlers/). The backend
handlers implement them for you.

## Backend options

| Option | Backend | Default | Meaning |
| ------ | ------- | ------- | ------- |
| `model` | Peewee | required | `peewee_aio` model |
| `manager` | Peewee | `model._manager` | `peewee_aio` manager used for queries |
| `model_pk` | Peewee | `model._meta.primary_key` | Primary key field |
| `delete_recursive` | Peewee | `False` | Delete related rows recursively |
| `table` | SQLAlchemy | required | `sqlalchemy.Table` |
| `database` | SQLAlchemy | required | `muffin_databases.Plugin` |
| `table_pk` | SQLAlchemy | `table.c.id` | Primary key column |

For Peewee the resource `name` defaults to `model._meta.table_name.lower()`; for SQLAlchemy to
`table.name`. A composite Peewee key is exposed as an `id` string joining the key parts with
`::` (for example `web::42`).

## Common options

| Option | Default | Meaning |
| ------ | ------- | ------- |
| `name` | table name | Resource name used in URLs and translations |
| `label` | `name` | Menu label |
| `group` | `None` | Menu group |
| `icon` | `""` | Material-UI icon name |
| `help` | `None` | Link to a resource help page |
| `columns` | all serialized fields | List-view columns, in order |
| `filters` | `()` | Fields shown in the list filter bar |
| `sorting` | `columns[0]` descending | Sortable fields; accepts strings and `(name, meta)` tuples |
| `limit` | `25` | Page size (cannot be `0`) |
| `limit_max` | `100` | Maximum page size accepted from the client |
| `limit_total` | `False` | Return the total count in list responses |
| `create` | `True` | Show the create screen and button |
| `edit` | `True` | Show the edit screen and button |
| `delete` | `True` | Show delete buttons |
| `show` | `True` | Show the detail screen |
| `id` | `"id"` | Name of the primary-key field |
| `ra_order` | `0` | Menu order; higher values come first when `menu_sort` is on |
| `actions` | discovered | Action list, filled from decorated methods |
| `locales` | `None` | Per-resource translations |

`filters` accepts field names, `Filter` instances from Muffin-REST
(`PWFilter`, `SAFilter`), and `(name, meta)` tuples:

```python
from muffin_admin import PWFilter

class Meta(PWAdminHandler.Meta):
    model = User
    filters = "is_active", ("email", {"operator": "$contains"}), PWFilter("role")
```

`sorting` and `filters` are the Muffin-REST options; see
[Querying](https://klen.github.io/muffin-rest/querying/) for operators and multi-field sorting.

When `sorting` is omitted and `columns` is not empty, the first column becomes the default
descending sort. For Peewee only real model fields are used for that default.

A filter on the primary key is added automatically unless you already listed it.

## Schemas

Screens and validation come from a marshmallow schema generated from the model or table. The
options:

| Option | Default | Meaning |
| ------ | ------- | ------- |
| `Schema` | generated | Use a ready schema instead of generating one |
| `schema_base` | backend schema | Base class for the generated schema (`ModelSchema`, `SQLAlchemyAutoSchema`) |
| `schema_fields` | `{}` | Extra fields added to the generated schema |
| `schema_meta` | `{}` | Options merged into the generated schema's `Meta` |
| `schema_unknown` | `ma.EXCLUDE` | Handling of unknown input keys |

```python
class Meta(PWAdminHandler.Meta):
    model = User
    schema_meta = {
        "load_only": ("password",),
        "dump_only": ("created",),
    }
    schema_fields = {
        "name": ma.fields.Function(lambda user: f"{user.first_name} {user.last_name}"),
    }
```

`load_only` fields never appear in the detail/list output; `dump_only` fields never appear in
create/edit forms. `schema_fields` is copied per resource, so subclasses do not share fields.

Field metadata drives the UI: `metadata["description"]` becomes `helperText`,
`metadata["label"]` becomes the input label, `required=True` marks the input as required, and
simple `load_default` values become `defaultValue`.

## react-admin overrides

These options shape the JSON sent to react-admin. Declare them as `ClassVar` on `Meta` when you
want the type checker to stay quiet; the runtime reads them as ordinary attributes.

| Option | Meaning |
| ------ | ------- |
| `ra_fields` | Field widget overrides for the list/show views |
| `ra_inputs` | Input widget overrides for create/edit and action forms |
| `ra_filters` | Filter widget overrides |
| `ra_filters_always_on` | Filter names rendered as always-on with a reset button |
| `ra_refs` | Foreign key display: `{source: {source, key, reference}}` |
| `ra_links` | Show-view links to related resources |
| `ra_list_params` | Extra properties merged into the `list` payload |
| `ra_show_params` | Extra properties merged into the `show` payload |

Each field or input override is either a widget name or a `(widget, props)` tuple:

```python
class Meta(PWAdminHandler.Meta):
    model = User
    ra_fields = {
        "picture": ("AvatarField", {"alt": "picture", "nameProp": "name", "sortable": False}),
    }
    ra_inputs = {"picture": ("ImgInput", {})}
    ra_filters = {
        "email": ("SearchFilter", {}),
        "created": ("DateRangeFilter", {"type": "datetime-local"}),
    }
    ra_filters_always_on = ["is_active"]
    ra_refs = {"group": {"source": "name"}}
    ra_links = (("message", {"label": "Messages", "title": "Show user messages"}),)
```

`ra_refs` keys are serialized field names. The backend fills in the rest: for a Peewee
`ForeignKeyField` it uses the related model's primary key and table name, for a SQLAlchemy
`ForeignKey` the referenced column and table. `reference` must match the resource name of the
related admin resource.

There is no `related_fields` option; related data is wired through `ra_refs` (for foreign keys)
and `ra_links` (for links on the detail page).

Defaults are chosen from the model/table where possible: Peewee choices become `SelectInput` /
`SelectField`, `TextField` becomes a multiline input, JSON fields become `JsonInput` /
`JsonField`, timestamps become `TimestampInput`, and SQLAlchemy enum columns become
`SelectInput`.

## Permissions

There are no per-resource permissions. Authorization is global: `@admin.check_auth` protects
the admin page, `ra.json` and the whole API. Use the `create`/`edit`/`delete`/`show` flags to
hide operations for everyone, and override hooks (`save`, `remove`, `prepare_collection`,
`prepare_resource`) to scope data per user:

```python
@admin.route
class MessageResource(PWAdminHandler):
    class Meta(PWAdminHandler.Meta):
        model = Message
        delete = False

    async def prepare_collection(self, request):
        query = await super().prepare_collection(request)
        return query.where(Message.user == request.user.id)
```

The frontend exposes a `getPermissions` identity role read from
`${auth_storage_name}_role` in the storage, but the bundled resources do not consume it.

## Hooks

`AdminHandler` adds two hooks to the Muffin-REST lifecycle:

| Hook | Meaning |
| ---- | ------- |
| `get_selected(request)` | Objects selected in a bulk action; the base returns the `ids` query values, the backends return a queryset |
| `log(request, response, action)` | Called after every request; no-op by default |

Everything else (`authorize`, `prepare_collection`, `prepare_resource`, `filter`, `sort`,
`paginate`, `load`, `dump`, `save`, `remove`) is the Muffin-REST lifecycle. See the
[API reference](api.md) for signatures.
