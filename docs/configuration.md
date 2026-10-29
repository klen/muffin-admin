# Configuration

Options come from the plugin defaults, the application config with the `ADMIN_` prefix,
keyword arguments of `Plugin(app, ...)`, and environment variables. Later sources win.

```python
from muffin_admin import Plugin

admin = Plugin(
    app,
    prefix="/admin",
    title="Shop admin",
    auth_storage="cookies",
)

# equivalent
app = Application("shop", ADMIN_TITLE="Shop admin", ADMIN_AUTH_STORAGE="cookies")
admin = Plugin(app)
```

## Options

| Option              | Config key               | Default                                             | Description |
| ------------------- | ------------------------ | --------------------------------------------------- | ----------- |
| `prefix`            | `ADMIN_PREFIX`           | `"/admin"`                                          | URL prefix of the admin. A trailing slash is stripped |
| `title`             | `ADMIN_TITLE`            | `"Muffin-Admin"`                                    | Page title and react-admin title |
| `main_js_url`       | `ADMIN_MAIN_JS_URL`      | `"{prefix}/main.js"`                                | Frontend bundle URL; `{prefix}` is substituted |
| `custom_js_url`     | `ADMIN_CUSTOM_JS_URL`    | `""`                                                | Extra script loaded after the bundle |
| `custom_css_url`    | `ADMIN_CUSTOM_CSS_URL`   | `""`                                                | Extra stylesheet for the page |
| `login_url`         | `ADMIN_LOGIN_URL`        | `None`                                              | Redirect target for cookie-mode authorization failures |
| `logout_url`        | `ADMIN_LOGOUT_URL`       | `None`                                              | Redirect target after logout; without it react-admin only clears local state |
| `menu_sort`         | `ADMIN_MENU_SORT`        | `True`                                              | Sort the resource menu: higher `ra_order` first, then by name |
| `auth_storage`      | `ADMIN_AUTH_STORAGE`     | `"localstorage"`                                    | `localstorage` or `cookies`; see [Authentication](auth.md) |
| `auth_storage_name` | `ADMIN_AUTH_STORAGE_NAME`| `"muffin_admin_auth"`                               | Key of the stored auth value |
| `app_bar_links`     | `ADMIN_APP_BAR_LINKS`    | `[{"url": "/", "icon": "Home", "title": "Home"}]`   | Links in the top bar; `icon` is a Material-UI icon name |
| `mutation_mode`     | `ADMIN_MUTATION_MODE`    | `"optimistic"`                                      | react-admin mutation mode: `pessimistic`, `optimistic` or `undoable` |
| `help`              | `ADMIN_HELP`             | `None`                                              | Link to a help page, shown on the dashboard |
| `locales`           | `ADMIN_LOCALES`          | `None`                                              | Translations merged with per-resource `locales`; see [Customization](customization.md#translations) |
| `secret`            | `ADMIN_SECRET`           | `None`                                              | Reserved. Nothing reads it; see below |
| `disabled`          | `ADMIN_DISABLED`         | `False`                                             | Turn the plugin off: `setup()` returns `False`, nothing is mounted and every admin route answers `404` |

`disabled` is inherited from Muffin's `BasePlugin`. Set it with `ADMIN_DISABLED=1`, `app` config
`ADMIN_DISABLED=True` or `admin.setup(app, disabled=True)`. `Plugin.setup()` then returns `False`,
the plugin is not registered in `app.plugins`, and neither the page, `ra.json`, `main.js`, nor
the `/api` routes are mounted.

`prefix` is used verbatim after the trailing slash is stripped, so `prefix="/"` mounts the
admin at the application root.

## Environment variables

Muffin prefixes plugin environment variables with the application config name (`CFG.NAME`,
`muffin` by default) and the plugin name:

```
{MUFFIN}_ADMIN_PREFIX
{MUFFIN}_ADMIN_TITLE
{MUFFIN}_ADMIN_AUTH_STORAGE
```

With the default `CFG.NAME="muffin"` that is `MUFFIN_ADMIN_TITLE`, not `ADMIN_TITLE`. Set a
name when one container serves one application and you want distinct prefixes:

```python
app = Application(NAME="shop")
# now reads SHOP_ADMIN_TITLE, SHOP_ADMIN_AUTH_STORAGE, ...
```

Values are JSON-decoded when possible, so lists and dictionaries fit in one variable:

```bash
export MUFFIN_ADMIN_TITLE="Shop admin"
export MUFFIN_ADMIN_AUTH_STORAGE="cookies"
export MUFFIN_ADMIN_APP_BAR_LINKS='[{"url": "/", "title": "Home", "icon": "Home"}]'
```

## About `secret`

`secret` exists in `Plugin.defaults` but no code reads it: neither the plugin, nor
`handler.py`, nor the frontend. Setting it changes nothing. Cookie storage writes the auth
value with `js-cookie` without signing or encrypting it, and the server never verifies a
signature. Treat the stored value as untrusted input:

- serve the admin over HTTPS;
- read the value in `check_auth` and validate it server-side (a session lookup, a signed
  token of your own, an external identity provider);
- keep `auth_storage="cookies"` for same-site setups; it sets a plain cookie with the default
  path.

The option is kept for backwards compatibility of the config surface and is documented here
so nobody assumes it enables signing.

## Options that change the page only

`title`, `custom_css_url`, `custom_js_url`, `main_js_url` and `prefix` are rendered into
`muffin_admin/admin.html` when `{prefix}` is requested. The rest is served to the frontend
through `{prefix}/ra.json`, together with the serialized resources and authorization state.
