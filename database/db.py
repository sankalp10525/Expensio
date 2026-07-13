import os
import sqlite3
from datetime import datetime

from werkzeug.security import generate_password_hash

# Absolute path to the SQLite file at the project root, so the DB is found
# regardless of the current working directory.
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "expense_tracker.db")

# Fixed set of expense categories used throughout the app.
CATEGORIES = ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"]


def get_db():
    """Open a connection to the SQLite database.

    Rows come back as dict-like ``sqlite3.Row`` objects and foreign-key
    enforcement is enabled on every connection.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables if they don't already exist. Safe to call repeatedly."""
    conn = get_db()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT NOT NULL,
            email         TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at    TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            amount      REAL NOT NULL,
            category    TEXT NOT NULL,
            date        TEXT NOT NULL,
            description TEXT,
            created_at  TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """
    )
    conn.commit()
    conn.close()


def seed_db():
    """Insert demo data for development. Idempotent: no-ops if users already exist."""
    conn = get_db()

    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0:
        conn.close()
        return

    cur = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123", method="pbkdf2:sha256")),
    )
    user_id = cur.lastrowid

    # Eight sample expenses covering every category, dated within the current
    # month (days 1-28 to stay valid for any month). Amounts are floats (₹).
    month = datetime.now().strftime("%Y-%m")
    expenses = [
        (user_id, 450.00, "Food", f"{month}-03", "Groceries for the week"),
        (user_id, 1200.50, "Transport", f"{month}-05", "Monthly metro pass"),
        (user_id, 2300.00, "Bills", f"{month}-07", "Electricity bill"),
        (user_id, 800.75, "Health", f"{month}-10", "Pharmacy"),
        (user_id, 650.00, "Entertainment", f"{month}-14", "Movie night"),
        (user_id, 3499.00, "Shopping", f"{month}-18", "New running shoes"),
        (user_id, 199.00, "Other", f"{month}-22", "Miscellaneous"),
        (user_id, 320.25, "Food", f"{month}-26", "Dinner with friends"),
    ]
    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) "
        "VALUES (?, ?, ?, ?, ?)",
        expenses,
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    seed_db()
    print(f"Initialized and seeded {DB_PATH}")
