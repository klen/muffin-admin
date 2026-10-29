# Custom actions

An action is a handler method decorated with `AdminHandler.action` (or the backend subclass).
The plugin renders a button for every decorated method, and the method becomes its own route
on the admin API.

```python
from muffin_admin import PWAdminHandler


@admin.route
class UserResource(PWAdminHandler):
    class Meta(PWAdminHandler.Meta):
        model = User

    @PWAdminHandler.action("/user/disable", label="Disable Users", view="bulk")
    async def disable_users(self, request, resource=None):
        """Mark selected users as inactive."""
        ids = request.query.getall("ids")
        await User.update(is_active=False).where(User.email << ids)
        return {"status": True, "ids": ids}

    @PWAdminHandler.action("/user/{id}/admin", view="show")
    async def mark_admin(self, request, resource=None):
        """Give the user the admin role."""
        resource.role = "admin"
        await resource.save()
```

Action paths are absolute inside the admin API, which is mounted at `{prefix}/api`. The
example above answers `POST /admin/api/user/disable` and `POST /admin/api/user/{id}/admin`.
Keep the resource name in the path; nothing prefixes it for you.

The method is called with `request` and a `resource` keyword argument. `resource` is the loaded
object for paths with `{id}` and `None` otherwise. Actions run through the regular handler
lifecycle, so `authorize`, `prepare_collection` and `prepare_resource` apply.

## Arguments

| Argument | Description |
| -------- | ----------- |
| `paths` | One or more URL paths for the action; the first matching path is used by the button |
| `methods` | HTTP methods allowed for the route, by default any method |
| `hosts` | A host name (or a list of names) to bind the route to |
| `view` | Where to show the button: `list`, `show`, `edit` or `bulk` (a string or a list) |
| `icon` | Material-UI icon name |
| `label` | Button label; the humanized method name by default |
| `schema` | Marshmallow schema; the admin renders a form and passes validated data as `data` |
| `help` | A link to an action help page |
| `confirm` | Ask for confirmation before the request, either `True` or a message |
| `file` | Serve the response as a file download (list and show views only) |

Any other keyword argument is passed to react-admin as an action property. It can override
generated ones, for example `title`:

```python
@PWAdminHandler.action("/user/greet", view="list", title="Say hello")
```

`view` decides which screens render the button:

- `list`: one button above the list, no selection needed.
- `show`: one button on the detail page; the path with `{id}` is used.
- `edit`: one button on the edit page.
- `bulk`: one button above the list acting on the selected rows; the selected ids are sent as
  the `ids` query parameter.

## Forms and validation

With a `schema`, the button opens a modal form built from the schema fields and sends the
validated payload to the method as `data`:

```python
import marshmallow as ma


class GreetSchema(ma.Schema):
    name = ma.fields.String(required=True)


@PWAdminHandler.action(
    "/user/greet",
    "/user/{id}/greet",
    label="Greeter",
    view=["list", "show"],
    schema=GreetSchema,
)
async def greet(self, request, resource=None, data=None):
    """Greet a user."""
    return {"status": True, "message": f"Hello {data.name}"}
```

Invalid or missing data answers `400` with the marshmallow messages in `errors`. The form
inputs follow the same field mapping used for create/edit; `metadata`, `required` and
`load_default` are honored, and `ra_inputs` overrides apply.

## Confirmation and feedback

- `confirm=True` asks "Do you confirm this action?" before sending.
- `confirm="message.key"` asks the translated message.
- A dict with `message` is shown as a success notification.
- A dict with `redirectTo` navigates there instead of refreshing the list.

## File downloads

`file=True` turns the button into a plain link, so the browser handles the response as a
download. Only `list` and `show` views support it; bulk actions ignore `file`.

```python
from muffin import Response


@PWAdminHandler.action(
    "/message/data.csv", label="Download CSV", icon="Download", view="list", file=True
)
async def csv(self, request, **_):
    """Download CSV file."""
    return Response(
        content="id,created,title\n" + "\n".join(f"{m.id},{m.created},{m.title}" for m in ...),
        content_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=messages.csv"},
    )
```

The download is a normal browser request: the frontend appends the stored token as the `t`
query parameter, and the current list filters as `where`. If you use `auth_storage="cookies"`,
the cookie is sent with the request as usual. In localstorage mode, read the token from
`request.query["t"]` in `check_auth`; see [Authentication](auth.md#file-downloads).

## Restricting method and host

```python
@PWAdminHandler.action(
    "/user/greet", methods=("POST",), hosts="example.com", view="list"
)
async def greet(self, request, resource=None):
    ...
```
