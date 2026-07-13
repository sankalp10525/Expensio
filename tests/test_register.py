from werkzeug.security import check_password_hash

import database.db as db


def _get_user(email):
    conn = db.get_db()
    try:
        return conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
    finally:
        conn.close()


def test_register_get_renders_form(client):
    resp = client.get("/register")
    assert resp.status_code == 200
    assert b"Create your account" in resp.data


def test_register_valid_creates_user_and_redirects(client):
    resp = client.post(
        "/register",
        data={"name": "Aarav", "email": "Aarav@Example.com", "password": "supersecret"},
    )
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/login")

    # Email is normalized to lowercase before storage.
    user = _get_user("aarav@example.com")
    assert user is not None
    assert user["name"] == "Aarav"
    # Password is hashed, never stored in plaintext.
    assert user["password_hash"] != "supersecret"
    assert user["password_hash"].startswith("pbkdf2:sha256")
    assert check_password_hash(user["password_hash"], "supersecret")


def test_register_duplicate_email_shows_error(client):
    data = {"name": "First", "email": "dupe@example.com", "password": "supersecret"}
    client.post("/register", data=data)

    resp = client.post(
        "/register",
        data={"name": "Second", "email": "dupe@example.com", "password": "anotherpass"},
    )
    assert resp.status_code == 200
    assert b"already exists" in resp.data

    # No second row was inserted for the duplicate email.
    conn = db.get_db()
    try:
        count = conn.execute(
            "SELECT COUNT(*) FROM users WHERE email = ?", ("dupe@example.com",)
        ).fetchone()[0]
    finally:
        conn.close()
    assert count == 1


def test_register_short_password_shows_error(client):
    resp = client.post(
        "/register",
        data={"name": "Shorty", "email": "short@example.com", "password": "1234567"},
    )
    assert resp.status_code == 200
    assert b"at least 8 characters" in resp.data
    assert _get_user("short@example.com") is None


def test_register_missing_fields_shows_error(client):
    resp = client.post(
        "/register",
        data={"name": "", "email": "", "password": ""},
    )
    assert resp.status_code == 200
    assert b"All fields are required" in resp.data
