from pathlib import Path

import pytest
from muffin import Application, TestClient

import muffin_admin


@pytest.fixture(
    params=["trio", "curio", pytest.param(("asyncio", {"loop_factory": None}), id="asyncio")]
)
def aiolib(request):
    return request.param


@pytest.fixture(scope="session", autouse=True)
def prebuild_js():
    main_js = Path(muffin_admin.__file__).parent.parent / "muffin_admin/main.js"
    original = main_js.read_bytes() if main_js.exists() else None
    main_js.write_text("console.log('muffin-admin js files');")
    yield main_js
    if original is None:
        main_js.unlink(missing_ok=True)
    else:
        main_js.write_bytes(original)


@pytest.fixture
def app():
    return Application(debug=True)


@pytest.fixture
def client(app):
    return TestClient(app)
