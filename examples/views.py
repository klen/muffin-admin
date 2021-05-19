"""Common views."""

from pathlib import Path

from muffin import ResponseFile


async def index(request):
    """Just a main page."""
    return """
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css">
    <div class="container p-3">
        <div class="alert alert-success" role="alert">
            <h4 class="alert-heading">Well done!</h4>
            <p>Aww yeah, you successfully run this example. Now you can open Admin Interface</p>
            <hr/>
            <p>Use <i>admin@admin.com:admin</i> to login</p>
            <a href="/admin" class="btn btn-success">Open Admin</a>
        </div>
    </div>

    """


async def admin_css(request):
    return ResponseFile(Path(__file__).parent / 'admin.css')
