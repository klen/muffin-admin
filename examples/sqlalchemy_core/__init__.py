"""Setup the application and plugins."""

from muffin import Application

from .. import views


# Create Muffin Application named 'example'
app = Application(name='example', debug=True)

app.route('/')(views.index)
app.route('/admin.css')(views.admin_css)

# Import the app's components
app.import_submodules()
