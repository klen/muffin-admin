import pytest
from muffin import Application, TestClient


@pytest.fixture(params=[
    'trio', 'curio', pytest.param(('asyncio', {'use_uvloop': False}), id='asyncio')])
def aiolib(request):
    return request.param


@pytest.fixture
def app():
    return Application(debug=True)


@pytest.fixture
def client(app):
    return TestClient(app)
