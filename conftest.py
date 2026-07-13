import pytest

import database.db as db
from app import app as flask_app


@pytest.fixture
def app(tmp_path, monkeypatch):
    """Flask app fixture (required by pytest-flask), backed by an isolated DB.

    Repoints ``database.db.DB_PATH`` at a fresh temp file so tests never touch
    the real ``expense_tracker.db``. ``get_db()`` reads ``DB_PATH`` at call
    time, so patching the module attribute is enough for the whole request.
    The schema is created fresh (and left unseeded) before each test.
    """
    test_db = tmp_path / "test.db"
    monkeypatch.setattr(db, "DB_PATH", str(test_db))
    db.init_db()

    flask_app.config.update(TESTING=True)
    yield flask_app
