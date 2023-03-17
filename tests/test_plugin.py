async def test_plugin(app):
    import muffin_admin

    assert app

    admin = muffin_admin.Plugin(app)
    assert admin

    data = admin.to_ra()
    assert data["apiUrl"]
    assert data["auth"] == {
        "storage": "localstorage",
        "storage_name": "muffin_admin_auth",
        "logoutURL": None,
        "loginURL": None,
    }


async def test_basic_files(app, client):
    import muffin_admin

    muffin_admin.Plugin(app)

    res = await client.get("/admin")
    assert res.status_code == 200
    text = await res.text()
    assert "Muffin-Admin Admin UI" in text

    res = await client.get("/admin/main.js")
    assert res.status_code == 200
    text = await res.text()
    assert "muffin-admin js files" in text


async def test_root_prefix(app, client):
    import muffin_admin

    admin = muffin_admin.Plugin(app, prefix="/")
    assert admin

    res = await client.get("/")
    assert res.status_code == 200
    text = await res.text()
    assert "Muffin-Admin Admin UI" in text

    res = await client.get("/main.js")
    assert res.status_code == 200
    text = await res.text()
    assert "muffin-admin js files" in text


async def test_auth(app, client):
    from muffin_rest import APIError

    from muffin_admin import Plugin

    admin = Plugin(app)

    res = await client.get("/admin/login")
    assert res.status_code == 404

    res = await client.get("/admin/ident")
    assert res.status_code == 404

    # Setup fake authorization process
    # --------------------------------

    @admin.check_auth
    async def authorize(request):
        auth = request.headers.get("authorization")
        if not auth:
            raise APIError.FORBIDDEN()

        return auth

    @admin.get_identity
    async def ident(request):
        user = request.headers.get("authorization")
        return {"id": user, "fullName": f"User-{user}"}

    @admin.login
    async def login(request):
        data = await request.data()
        return data.get("username", False)

    auth = admin.to_ra()["auth"]
    assert auth
    assert auth == {
        "authorizeURL": "/admin/login",
        "identityURL": "/admin/ident",
        "loginURL": None,
        "logoutURL": None,
        "required": True,
        "storage": "localstorage",
        "storage_name": "muffin_admin_auth",
    }

    res = await client.get("/admin/login", data={"username": "user", "password": "pass"})
    assert res.status_code == 200
    assert await res.text() == "user"

    res = await client.get("/admin/ident", headers={"authorization": "user"})
    assert res.status_code == 200
    assert await res.json() == {"id": "user", "fullName": "User-user"}

    res = await client.get("/admin")
    assert res.status_code == 403


async def test_dashboard(app, client):
    import muffin_admin

    admin = muffin_admin.Plugin(app)

    @admin.dashboard
    async def dashboard(request):
        """Render admin dashboard cards."""
        return [
            {"name": "application config", "value": {k: str(v) for k, v in app.cfg}},
            {"name": "request headers", "value": dict(request.headers)},
        ]

    res = await client.get("/admin/ra.json")
    assert res.status_code == 200
    data = await res.json()
    assert data["dashboard"]
    assert data["dashboard"][0]["name"] == "application config"
    assert data["dashboard"][1]["name"] == "request headers"
