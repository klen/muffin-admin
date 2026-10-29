# Customization

## CSS and JavaScript

`custom_css_url` and `custom_js_url` are injected into `admin.html`, next to the bundle:

```python
admin = Plugin(
    app,
    custom_css_url="/static/admin.css",
    custom_js_url="/static/admin-extra.js",
)
```

The CSS link is placed in `<head>` and the script after the main bundle, so custom JavaScript
can extend the admin before it initializes. Keep both values to a plain URL: they are inserted
into the HTML body as-is. [Custom frontend](frontend.md) explains the load order and what a
script can do with it.

To replace the bundle entirely, point `main_js_url` at another build:

```python
admin = Plugin(app, main_js_url="https://cdn.example.com/admin/main.js")
```

The default `{prefix}/main.js` is served from the package. It is built from `frontend/` and is
not committed; a checkout without a built bundle answers `500` for that route.

Replacing the bundle with your own application, or extending the stock one with JavaScript, is
described in [Custom frontend](frontend.md).

## Translations

`locales` is a mapping of language code to react-admin messages, deep-merged with each
resource's `Meta.locales`. Resource translations override the plugin ones.

```python
admin = Plugin(
    app,
    locales={
        "en": {"resources": {"user": {"fields": {"name": "Full Name"}}}},
        "ru": {"resources": {"user": {"name": "Пользователи"}}},
    },
)


@admin.route
class UserResource(PWAdminHandler):
    class Meta(PWAdminHandler.Meta):
        model = User
        locales = {
            "en": {"groups": {"People": "Users"}},
            "ru": {"groups": {"People": "Пользователи"}},
        }
```

The keys are react-admin translation keys, relative to the language:

| Key | Used for |
| --- | -------- |
| `resources.<name>.name` | Resource name in the menu and titles |
| `resources.<name>.fields.<field>` | Field labels |
| `resources.<name>.actions.<action id>` | Action labels (action id is the method name) |
| `groups.<group>` | Menu group names |

`label` in an action can also be a translation key, for example `label="ra.action.export"`.

## Help links

There are two independent help links:

- `Plugin(app, help="...")`: shown on the dashboard.
- `Meta.help = "..."` on a resource: shown on the resource screens.
- `action(..., help="...")`: shown in the action form.

## Mutation mode

`mutation_mode` is passed to react-admin's `Admin` component:

```python
admin = Plugin(app, mutation_mode="pessimistic")
```

| Value | Behavior |
| ----- | -------- |
| `optimistic` (default) | Update the UI immediately, roll back on error |
| `pessimistic` | Wait for the server before updating the UI |
| `undoable` | Show an undo notification, send the request after a delay |

## Top bar

`app_bar_links` adds links to the top bar; each entry needs `url` and `title`, and optionally
an `icon` (Material-UI name):

```python
admin = Plugin(
    app,
    app_bar_links=[
        {"url": "/", "icon": "Home", "title": "Home"},
        {"url": "/docs", "icon": "Description", "title": "Docs"},
    ],
)
```

`menu_sort` controls whether resources are sorted by `ra_order` and name.

## Building the frontend

The bundle comes from `frontend/` and is written to `muffin_admin/main.js` by webpack:

```bash
make -C frontend          # install deps if needed, then webpack
make -C frontend dev      # webpack dev server on :5555 proxying the backend
make -C frontend watch    # rebuild on change
make -C frontend lint     # tsc --noEmit
```

`make -C frontend` only bundles; it does not copy anything into `docs/` or run Python tests.
The release workflow runs `make pypi` in `frontend/` before `uv build`, so the wheel and sdist
pick up the freshly built `main.js` and `main.js.LICENSE.txt`.

The Python package includes whatever `main.js` is on disk at build time. A plain `uv build`
from a clean checkout produces a package without the bundle; see
[Development](development.md#release) for the release path.
