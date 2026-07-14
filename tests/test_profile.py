from datetime import datetime

import database.db as db

EMAIL = "member@example.com"
PASSWORD = "supersecret"
NAME = "Test Member"


def _make_user():
    """Create a user directly in the (isolated) test DB and return its id."""
    return db.create_user(NAME, EMAIL, PASSWORD)


def test_profile_logged_out_redirects_to_login(client):
    resp = client.get("/profile")
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/login")
    # No user data should leak in the redirect response.
    assert NAME.encode() not in resp.data
    assert EMAIL.encode() not in resp.data


def test_profile_logged_in_renders_name_and_email(client):
    _make_user()
    client.post("/login", data={"email": EMAIL, "password": PASSWORD})

    resp = client.get("/profile")
    assert resp.status_code == 200
    assert NAME.encode() in resp.data
    assert EMAIL.encode() in resp.data


def test_profile_does_not_leak_password_hash(client):
    _make_user()
    client.post("/login", data={"email": EMAIL, "password": PASSWORD})

    resp = client.get("/profile")
    user = db.get_user_by_email(EMAIL)
    assert user["password_hash"].encode() not in resp.data


def test_profile_shows_member_since(client):
    _make_user()
    client.post("/login", data={"email": EMAIL, "password": PASSWORD})

    resp = client.get("/profile")
    assert b"Member since" in resp.data
    # created_at defaults to now, so the actual formatted join date renders
    # (not the "—" fallback used when created_at is missing/unparseable).
    user = db.get_user_by_email(EMAIL)
    expected = datetime.strptime(
        user["created_at"], "%Y-%m-%d %H:%M:%S"
    ).strftime("%-d %B %Y")
    assert expected.encode() in resp.data
