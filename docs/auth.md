# Authentication

Without authorization callbacks the admin is open: `/admin`, `ra.json` and the whole API are
served to anyone. `Plugin.check_auth` turns authorization on for all of them.

```python
from muffin_admin import Plugin

admin = Plugin(app)


@admin.check_auth
async def auth(request):
    """Return the current user, or raise when there is none."""
    token = request.headers.get("authorization")
    user = await User.select().where(User.email == token).first()
    if not user:
        raise APIError.FORBIDDEN()
    return user
```

`check_auth` stores the callback on the Muffin-REST API (`api.authorize`) and sets
`auth["required"] = True` in `ra.json`. Every resource request calls it first; Muffin-REST
answers `403` when the callback raises. The value it returns becomes `self.auth` in the
handler, which is how `prepare_collection` and other hooks can scope data to the user.

The callback also receives file-download requests; see [File downloads](#file-downloads).

## Identity

`@admin.get_identity` returns the user object react-admin shows in the top bar. It is called
with the original request after login:

```python
@admin.get_identity
async def ident(request):
    """Get current user information."""
    user = await auth(request)
    if user:
        return {"id": user.pk, "fullName": user.name, "avatar": user.picture}
```

`id`, `fullName` and `avatar` are the fields react-admin reads. Without `get_identity` the
admin never calls `/admin/ident` and only keeps the login token.

## Login and logout

`@admin.login` implements the login page. It receives the form data and must return the value
that is stored as the auth token:

```python
from muffin import ResponseJSON
from muffin_rest import APIError


@admin.login
async def login(request):
    """Login a user."""
    data = await request.data()
    user = await User.select().where(
        User.email == data["username"], User.password == data["password"]
    ).first()
    if not user:
        raise APIError.UNAUTHORIZED()
    return ResponseJSON(user.email)
```

Return a string token. An object is stringified when stored, so a scalar (email, session id,
JWT) is what the frontend sends back as the credential. To reject the credentials, raise an HTTP
error (`APIError.UNAUTHORIZED`, `ResponseError.FORBIDDEN`, ...): the admin keeps whatever the
endpoint returns, so returning `null` with status `200` stores the string `"null"` instead of
failing the login.

The login and identity routes answer `404` until the decorators are applied.

There is no server-side logout route. On logout the frontend clears the stored value and, when
`logout_url` is configured, navigates to it:

```python
admin = Plugin(app, logout_url="/logout")
```

## Storage

`auth_storage` chooses where the browser keeps the token:

| Value | Stored in | Sent as |
| ----- | --------- | ------- |
| `localstorage` (default) | `localStorage[auth_storage_name]` | `Authorization` header on API and file requests |
| `cookies` | cookie `auth_storage_name` via `js-cookie` | cookie on every request |

In `cookies` mode the server decides what to do with the cookie, because `check_auth` is the
only code that validates it:

```python
admin = Plugin(app, auth_storage="cookies", auth_storage_name="shop_auth")


@admin.check_auth
async def auth(request):
    token = request.cookies.get("shop_auth")
    ...
```

In `cookies` mode the plugin also guards the HTML page and `ra.json`: when `check_auth`
returns a falsy value, both redirect to `login_url` (or `/` when it is unset). Raising an
`APIError` still produces that error instead of a redirect. In `localstorage` mode the page is
served before the token is checked, and the frontend redirects itself to the login screen.

The cookie is a plain cookie: no signature, no encryption, no `HttpOnly`. `admin.secret` does
not sign it; the option is unused. Use HTTPS, keep the cookie short-lived, and validate it
server-side. See [`secret`](configuration.md#about-secret).

## File downloads

A file action downloads the response with `fetch`, using the same `Authorization` header as
normal API calls. The current list filters are sent as the `where` query parameter:

```
/admin/api/message/data.csv?f&where=...
```

`check_auth` reads the token from the header, exactly like other requests:

```python
token = request.headers.get("authorization")
```

With `auth_storage="cookies"` the cookie is sent automatically.

## Roles

`@admin.check_auth` is the only server-side check. The frontend exposes a `getPermissions`
identity role read from `${auth_storage_name}_role` in the storage, but the bundled resources
do not use it: there are no per-resource permissions. Hide operations with `create`, `edit`,
`delete` and `show` in `Meta`, and scope data in handler hooks.

## Putting it together

```python
from muffin import ResponseJSON
from muffin_rest import APIError

from muffin_admin import Plugin, PWAdminHandler

admin = Plugin(app)


@admin.check_auth
async def auth(request):
    token = request.headers.get("authorization")
    user = await User.select().where(User.email == token).first()
    if not user:
        raise APIError.FORBIDDEN()
    return user


@admin.get_identity
async def ident(request):
    user = await auth(request)
    return {"id": user.email, "fullName": user.email}


@admin.login
async def login(request):
    data = await request.data()
    user = await User.select().where(
        User.email == data["username"], User.password == data["password"]
    ).first()
    if not user:
        raise APIError.UNAUTHORIZED()
    return ResponseJSON(user.email)
```

The complete version with a Peewee model lives in `example/peewee_orm/admin.py`.
