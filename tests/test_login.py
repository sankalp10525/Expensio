import database.db as db

EMAIL = "member@example.com"
PASSWORD = "supersecret"
NAME = "Test Member"


def _make_user():
    """Create a user directly in the (isolated) test DB and return its id."""
    return db.create_user(NAME, EMAIL, PASSWORD)


def test_login_get_renders_form(client):
    resp = client.get("/login")
    assert resp.status_code == 200
    assert b"Welcome back" in resp.data


def test_login_valid_sets_session_and_redirects(client):
    user_id = _make_user()

    resp = client.post("/login", data={"email": EMAIL, "password": PASSWORD})
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/profile")

    with client.session_transaction() as sess:
        assert sess.get("user_id") == user_id
        assert sess.get("user_name") == NAME


def test_login_email_is_case_insensitive(client):
    _make_user()
    # Registration lowercases emails; login should normalize the same way.
    resp = client.post("/login", data={"email": "Member@Example.com", "password": PASSWORD})
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/profile")


def test_login_wrong_password_rejected(client):
    _make_user()

    resp = client.post("/login", data={"email": EMAIL, "password": "wrongpass"})
    assert resp.status_code == 200
    assert b"Invalid email or password." in resp.data
    with client.session_transaction() as sess:
        assert "user_id" not in sess


def test_login_unknown_email_rejected(client):
    resp = client.post("/login", data={"email": "nobody@example.com", "password": PASSWORD})
    assert resp.status_code == 200
    assert b"Invalid email or password." in resp.data
    with client.session_transaction() as sess:
        assert "user_id" not in sess


def test_login_preserves_email_on_error(client):
    resp = client.post("/login", data={"email": EMAIL, "password": "wrongpass"})
    assert resp.status_code == 200
    assert EMAIL.encode() in resp.data  # email echoed back into the form


def test_logout_clears_session_and_redirects(client):
    _make_user()
    client.post("/login", data={"email": EMAIL, "password": PASSWORD})

    resp = client.get("/logout")
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/")
    with client.session_transaction() as sess:
        assert "user_id" not in sess


def test_navbar_reflects_auth_state(client):
    _make_user()

    # Logged out: shows Sign in / Get started.
    resp = client.get("/")
    assert b"Sign in" in resp.data
    assert b"Logout" not in resp.data

    # Logged in: shows Profile / Logout.
    client.post("/login", data={"email": EMAIL, "password": PASSWORD})
    resp = client.get("/")
    assert b"Logout" in resp.data
    assert b"Sign in" not in resp.data
