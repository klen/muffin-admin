# Dashboard

`@admin.dashboard` fills the start page. The callback receives the `ra.json` request and
returns cards; each card is a dict with a `title` and a `value`.

```python
from muffin_admin import Plugin

admin = Plugin(app)


@admin.dashboard
async def dashboard(request):
    """Render dashboard cards."""
    return [
        [
            {"title": "App config", "value": [(key, str(value)) for key, value in app.cfg]},
            {"title": "Request headers", "value": dict(request.headers)},
        ],
    ]
```

## Layout

The return value is a list of blocks. A list inside the list is a row of cards; nesting makes
another group. A single dict also works and renders one card.

```python
return [
    [card, card],   # first row
    [card, card],   # second row
]

return [card]       # one row with one card
return card         # one card
```

`value` decides how the card body is rendered:

- a list of lists is rendered as a table, one inner list per row;
- any other value is rendered as JSON in a `<pre>` block.

That is why the app config is converted to `(key, value)` pairs (a table) while request headers
are passed as a dict (JSON).

## Notes

The callback runs on every `{prefix}/ra.json` request, which the admin makes on page load.
Keep it cheap and do not mutate shared state. It is only called when a dashboard is registered;
without it the frontend renders the default start page.

The plugin-level `help` option adds a link on the dashboard, next to the dashboard actions:

```python
admin = Plugin(app, help="https://example.com/admin-help")
```
