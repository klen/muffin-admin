# Custom frontend

The plugin ships a compiled react-admin application in `muffin_admin/main.js`. It renders
whatever `{prefix}/ra.json` describes, so most projects never touch the frontend. This page
covers the cases where you do, from a small patch of the stock page up to a separate
single page application built on the published `muffin-admin` npm package.

The Python side and the browser side are independent: Python serves the resource description
and the REST API, the browser runs a bundle. Replacing the bundle does not change the plugin,
and changing the plugin does not require a frontend build.

## When the stock bundle is enough

The stock bundle is enough when the screens you need can be described by `AdminHandler.Meta`:
fields, filters, actions, a dashboard, translations. All of that is data, and
[Resources](resources.md), [Custom actions](actions.md) and [Dashboard](dashboard.md) cover it.

You need your own build when you want something the description cannot express:

- components that do not map to a react-admin field or input (custom charts, editors, wizards);
- your own authorization flow, identity, or a token stored somewhere else;
- branding beyond a title, a stylesheet and app bar links;
- static files deployed on their own host, container or release cadence.

## Three levels of customization

| Level | What you write | What you build |
| ----- | -------------- | -------------- |
| Options | `Plugin(app, ...)` | nothing |
| `custom_js_url` | one plain JavaScript file | nothing |
| Own SPA | a React application on the `muffin-admin` package | your own bundle |

### 1. Options only

```python
admin = Plugin(
    app,
    title="Shop admin",
    custom_css_url="/static/admin.css",
    custom_js_url="/static/admin-extra.js",
    app_bar_links=[{"url": "/docs", "icon": "Description", "title": "Docs"}],
    help="https://example.com/admin-help",
    locales={"ru": {"resources": {"user": {"name": "Пользователи"}}}},
)
```

`title`, `custom_css_url`, `custom_js_url` and `main_js_url` are rendered into the page
template, the rest travels in `ra.json`. See [Configuration](configuration.md) for every
option. `main_js_url` already lets you swap the bundle for your own build of the same entry
point, as long as that build sets `globalThis.initAdmin`.

### 2. `custom_js_url`: patch the page after the bundle

The template loads the bundle, then the custom script, then calls the initializer:

```html
<script src="/admin/main.js"></script>
<script src=/static/admin-extra.js></script>
<script> initAdmin('/admin') </script>
```

The bundle is built from `frontend/src/web.ts`, which only does
`globalThis.initAdmin = initAdmin`. So the custom script runs after `initAdmin` exists and
before it is called, and it may replace it:

```js
// /static/admin-extra.js
const bundleInit = globalThis.initAdmin

globalThis.initAdmin = (prefix) => {
  console.info("muffin-admin: booting", prefix)
  return bundleInit(prefix)
}
```

The same window lets you wrap `fetch` and edit the `ra.json` response before the stock
application reads it. What you cannot do from here is render a different React tree: the bundle
exposes `initAdmin` and nothing else. For that use the npm package.

Two details of the option:

- the value is inserted into the template as-is, without quotes, so keep it a plain URL with no
  spaces or quotes;
- the plugin renders the tag only. It does not serve the file: put it in the application's
  static files (`STATIC_FOLDERS` / `STATIC_URL_PREFIX`) or on a CDN.

The order of the tags is covered by `tests/test_plugin.py::test_custom_assets_order`.

### 3. Own SPA

The rest of this page.

## Own SPA

In this setup the Python part is an API only: the plugin is mounted under an API prefix and
serves `ra.json` plus the REST API, while the HTML and the bundle come from your own container.

### Install the package

```bash
npm i muffin-admin
```

The package is built from the same sources as the stock bundle, compiled to `dist/` by `tsc`.
It exports:

| Export | Purpose |
| ------ | ------- |
| `MuffinAdmin` | The application component; reads everything from the context |
| `MuffinAdminContext` | Context with the `ra.json` payload (`AdminOpts`) |
| `setupAdmin`, `buildAdmin`, `findBuilder` | Slot registry, see [Slots](#slots) |
| `requestHeaders`, `makeRequest` | Mutable headers and the fetch wrapper used for every API call |
| `initAdmin` | The stock bootstrap: fetch `ra.json` and render into `#root` |
| `buildRA`, `buildRAComponent` | Turn a serialized field or input description into a component |
| `useMuffinAdminOpts`, `useMuffinResourceOpts`, `useAction` | Hooks for your components |
| `ActionButton`, `LinkButton`, `CopyButton`, `LinkAction` | Buttons from the stock screens |
| `AdminOpts`, `AdminResourceProps`, `AdminAction`, `AdminField`, `AdminInput`, `AdminShowProps`, `TAdminType`, `TAdminPath` | Types |

`MuffinAdmin` takes the usual react-admin `AdminProps`; `authProvider`, `dataProvider`,
`i18nProvider`, `layout` and `loginPage` are built from the context value unless you pass your
own.

### Bootstrap

The only input the application needs is the `ra.json` payload. Its URL is the *plugin* prefix,
not the static one: with `Plugin(app, prefix="/api/manage")` it lives at
`/api/manage/ra.json`, and the `apiUrl` inside it points at `/api/manage/api`.

```tsx
// src/App.tsx
import { type AdminOpts, MuffinAdmin, MuffinAdminContext, requestHeaders } from "muffin-admin"
import { useEffect, useState } from "react"

const API_PREFIX = process.env.API_PREFIX // "/api/manage"

export function App() {
  const [opts, setOpts] = useState<AdminOpts | null>(null)

  useEffect(() => {
    requestHeaders.Authorization = `Bearer ${readToken()}`
    fetch(`${API_PREFIX}/ra.json`, { headers: requestHeaders })
      .then((res) => res.json())
      .then(setOpts)
  }, [])

  if (!opts) return null
  return (
    <MuffinAdminContext.Provider value={opts}>
      <MuffinAdmin disableTelemetry />
    </MuffinAdminContext.Provider>
  )
}
```

`requestHeaders` is a plain mutable object merged into the headers of every request the package
makes, so setting it once covers the resource API and the actions. `disableTelemetry` is
already set in `ra.json` by the plugin; passing it again is harmless.

Where the token comes from is your business. The stock application uses the
[`auth-storage-get` and `auth-storage-set`](#slots) slots for it: `get` returns a function that
reads the stored credential, `set` returns a function that writes it. The default
implementations use `localStorage[auth_storage_name]` or the cookie, according to
`auth_storage` in `ra.json`.

### Slots

`setupAdmin([type, ...ids], builder)` registers a component for a place in the UI. The path is
`[type, ...ids]`: the type comes from `TAdminType`, the ids narrow it to a resource, an action
or a locale. `findBuilder` looks the exact path up and drops the last id until something
matches, so a shorter path is a fallback:

```tsx
setupAdmin(["show-fields"], () => <TextField source="email" />)        // every resource
setupAdmin(["show-fields", "user"], () => <TextField source="name" />) // only "user"
```

Register before rendering: the registry is a map read at render time, so a late
`setupAdmin` does not re-render mounted screens.

Global slots:

| Path | Builder gets | Replaces |
| ---- | ------------ | -------- |
| `["admin"]` | — | The application component; registered by the package and never looked up |
| `["auth-provider"]` | `ra.json` `auth` | react-admin `AuthProvider` factory |
| `["auth-storage-get"]` | `ra.json` `auth` | Function returning a function that reads the stored credential |
| `["auth-storage-set"]` | `ra.json` `auth` | Function returning `(name, value) => void` that writes it |
| `["data-provider"]` | `apiUrl` | react-admin `DataProvider` factory |
| `["layout"]` | — | react-admin `Layout` |
| `["appbar"]` | — | Top bar inside the layout |
| `["menu"]` | — | Side menu |
| `["loginpage"]` | — | Login page |
| `["dashboard"]` | — | The whole dashboard |
| `["dashboard-actions"]` | — | Buttons row at the top of the dashboard |
| `["dashboard-content"]` | — | Cards area of the dashboard |
| `["locale", locale]` | — | Messages for one locale, merged over the built-in and backend ones |
| `["resource", name]` | `{name}` | One resource: wraps the create, edit, list and show views |

Per-resource slots (`name` is the resource name from `ra.json`):

| Path | Replaces |
| ---- | -------- |
| `["create"]`, `["create-toolbar"]`, `["create-inputs"]` | Create view, its toolbar, its inputs |
| `["edit"]`, `["edit-toolbar"]`, `["edit-actions"]`, `["edit-form-toolbar"]`, `["edit-inputs"]` | Edit view, modal header, buttons in the header, form buttons, form inputs |
| `["list"]`, `["list-toolbar"]`, `["list-actions"]`, `["list-grid"]` | List view, its toolbar, bulk actions, the datagrid |
| `["list-fields"]`, `["list-grid-buttons"]`, `["list-filters"]` | Datagrid columns, extra datagrid cells, filter inputs |
| `["show"]`, `["show-toolbar"]`, `["show-actions"]`, `["show-links"]`, `["show-fields"]` | Show view, its toolbar, its buttons, the links under the toolbar, its fields |
| `["action-form", actionId, name]` | Payload form of one action button |

The builders receive what the default implementation needs: `list-fields`, `list-filters` and
`create-inputs` get the serialized array from `ra.json` (`AdminField[]` / `AdminInput[]`),
`show-fields` gets the show object (`{fields, links, edit}`), the rest get no props. A few
examples:

```tsx
// list-fields: the datagrid columns
setupAdmin(["list-fields", "user"], () => (
  <>
    <TextField source="email" />
    <TextField source="name" />
  </>
))

// show-fields: the fields on the show screen
setupAdmin(["show-fields", "user"], () => <TextField source="email" />)

// edit-inputs: the inputs of the edit form
setupAdmin(["edit-inputs", "user"], () => (
  <>
    <TextInput source="name" />
    <BooleanInput source="is_active" />
  </>
))

// list-grid-buttons: extra cells after the columns
function CopyID() {
  const record = useRecordContext()
  return <CopyButton value={record?.id} />
}
setupAdmin(["list-grid-buttons", "user"], () => <CopyID />)

// dashboard-content: an extra card on the start page
setupAdmin(["dashboard-content"], () => (
  <Card>
    <CardContent>Custom block</CardContent>
  </Card>
))

// locale: translations for one language, in react-admin key format
setupAdmin(["locale", "ru"], () => ({
  resources: { user: { name: "Пользователи", fields: { is_active: "Активен" } } },
}))

// auth-storage-get: read the credential from wherever you keep it
setupAdmin(["auth-storage-get"], () => () => localStorage.getItem("shop-token"))
```

### Build config

Two values are needed at build time: the static prefix (for asset URLs) and the API prefix
(for the `ra.json` URL). Keep them in `.env.default` and inline them into the bundle.

```js
// webpack.config.js
const webpack = require("webpack")
const HtmlWebpackPlugin = require("html-webpack-plugin")

const mode = process.env.NODE_ENV || "production"

module.exports = {
  mode,
  entry: "./src/index.tsx",
  output: { filename: "[name].[contenthash].js", path: path.resolve(__dirname, "dist") },
  plugins: [
    new HtmlWebpackPlugin({
      publicPath: mode == "development" ? "/" : `${process.env.ADMIN_PREFIX}/`,
      templateContent: `<html><body><div id="root"></div></body></html>`,
    }),
    new webpack.EnvironmentPlugin(["ADMIN_PREFIX", "API_PREFIX"]),
  ],
  devServer: {
    proxy: [{ context: ["/api"], target: process.env.DEV_BACKEND }],
  },
}
```

In development `publicPath` is `/` because the dev server serves the assets itself; in
production it is `ADMIN_PREFIX`, so the same build works under `/admin/`. The dev server proxy
sends `ra.json` and the REST API to the backend, which keeps the SPA on `:8080` free of CORS.

With Vite the same two values go into `define`, and `process.env.NODE_ENV` must be defined too:
the package reads it in `buildAdmin`/`findBuilder` and a bare `process` is not available there.

```js
export default defineConfig({
  base: mode == "development" ? "/" : `${env.ADMIN_PREFIX}/`,
  define: {
    "process.env.NODE_ENV": JSON.stringify(mode),
    "process.env.ADMIN_PREFIX": JSON.stringify(env.ADMIN_PREFIX),
    "process.env.API_PREFIX": JSON.stringify(env.API_PREFIX),
  },
})
```

### Deploy

The built `dist/` is served by your own container or CDN under the static prefix; the Python
application keeps its own prefix and serves only what the SPA asks for: `ra.json` and the API.

```python
admin = Plugin(app, prefix="/api/manage", login_url="/auth/login", logout_url="/auth/logout")
```

`check_auth` guards the REST API and, in cookie mode, also the page and `ra.json`;
`get_identity` provides the identity for the top bar. Both are the same callbacks as in
[Authentication](auth.md). The plugin also mounts its own page at `/api/manage` and a
`main.js` route there; nothing uses them in this setup.

A reverse proxy sends `PathPrefix("/admin")` to the static container and `PathPrefix("/api")` to
the application, so the browser sees one origin and no CORS configuration is needed:

```yaml
# the static container
- traefik.http.routers.admin.rule=Host(`example.com`) && PathPrefix(`/admin`)
- traefik.http.services.admin.loadbalancer.server.port=80

# the application
- traefik.http.routers.api.rule=Host(`example.com`) && PathPrefix(`/api`)
```

nginx works the same way: serve `dist/` for `/admin/` with a fallback to `index.html` for the
router paths, and proxy `/api/` to the application.

### Pitfalls

- `main_js_url` and `custom_js_url` only render script tags. The plugin serves exactly one
  file, `{prefix}/main.js`, from the package directory.
- `admin.html` is read when the package is imported, so the page layout is fixed for the life
  of the process and cannot be overridden per application.
- Without a built bundle the page renders, but `{prefix}/main.js` answers `500` (the file
  response fails on a missing file) and nothing initializes.
- With `auth_storage` other than `cookies`, `check_auth` protects the API but not the page and
  not `{prefix}/ra.json`: the resource description is public. See
  [Authentication](auth.md#storage).
- `muffin-admin` lists `react` and `react-admin` in `dependencies`, not in `peerDependencies`.
  npm deduplicates them when your ranges match; a mismatch leaves two copies of React in the
  bundle.
- The default `auth-storage-get` reads `auth_storage_name` from `localStorage` and overwrites
  `requestHeaders.Authorization` at render time when it finds a value. If your token lives
  elsewhere, override that slot so both agree.

## Building muffin-admin itself

For contributors to this repository, the stock bundle is built from `frontend/`:

```bash
make -C frontend        # yarn install if needed, then webpack -> muffin_admin/main.js
```

Webpack writes `muffin_admin/main.js` (and `main.js.LICENSE.txt`) next to the Python package,
which is where the plugin serves it from. Both files are gitignored
(`/muffin_admin/main.js*`), so a fresh checkout has no bundle until you build one.

The release workflow does the same in `frontend/` with `make pypi` (installs, compiles the npm
package into `frontend/dist/`, then bundles), publishes the npm package, and only then runs
`uv build`. `uv_build` packs everything under `muffin_admin/`, so the wheel and sdist contain
the bundle. See [Development](development.md#release) for the release path.
