"""Setup the application and plugins."""

from muffin import Application


# Create Muffin Application named 'example'
app = Application(name='example', debug=True)

# Import the app's components
app.import_submodules()
