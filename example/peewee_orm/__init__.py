"""Setup the application and plugins."""

from pathlib import Path

from muffin import Application

from example import views

# Create Muffin Application named 'example'
app = Application(
    name="example", debug=True, static_folders=[Path(__file__).parent.parent / "static"]
)

app.route("/")(views.index)
app.route("/admin.css")(views.admin_css)

# Import the app's components
app.import_submodules()
