<div align="center">

# ◈ Expensio

### Track every rupee. Know where it goes.

A clean, minimal personal **expense tracker** — built with Flask, SQLite, and server-rendered Jinja templates.
No frameworks on the frontend, no ORM on the backend. Just readable, hand-written code.

<br>

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/status-in%20development-orange)

</div>

---

## 📑 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Screenshots](#-screenshots)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Database](#-database)
- [Build Roadmap](#-build-roadmap)
- [Conventions](#-conventions)
- [Testing](#-testing)
- [License](#-license)

---

## 📖 About

**Expensio** is a personal finance web app that lets you log expenses, categorize them, and review
where your money goes — without the spreadsheet headache.

> ⚠️ **Note:** This repo is a **step-by-step teaching scaffold**, not a finished application.
> Much of the functionality is intentionally left as designated placeholders to be built in a fixed
> order (see the [Build Roadmap](#-build-roadmap)). The architecture and styling are complete; the
> feature logic is filled in one step at a time.

---

## ✨ Features

| | Feature | Status |
|---|---|:---:|
| ₹ | **Log expenses instantly** — amount, category, date, and description in one simple form | 🚧 |
| ◎ | **Understand your patterns** — category breakdowns and monthly summaries | 🚧 |
| ◷ | **Filter by time period** — view spending for any date range | 🚧 |
| 🔐 | **Accounts** — register, sign in, profile | 🚧 |
| 🌗 | **Light / dark theme** — with persisted preference and no flash-of-wrong-theme | ✅ |
| 🗄️ | **SQLite data layer** — schema, seeding, foreign-key enforcement | ✅ |
| 📄 | **Landing, Terms & Privacy pages** | ✅ |

<sub>✅ done · 🚧 in progress / scaffolded</sub>

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.9+, [Flask](https://flask.palletsprojects.com/) 3.1 |
| **Database** | SQLite 3 (via the stdlib `sqlite3` module — no ORM) |
| **Templating** | Jinja2 with template inheritance |
| **Auth hashing** | `werkzeug.security` (PBKDF2-SHA256) |
| **Styling** | Hand-written CSS (`static/css/style.css`) — no framework |
| **Frontend JS** | Vanilla JS (`static/js/main.js`) — theme toggle + video modal |
| **Fonts** | DM Sans + DM Serif Display (Google Fonts) |
| **Testing** | pytest + pytest-flask |

---

## 🖼 Screenshots

> _Add screenshots to a `docs/` folder and reference them here, e.g._
>
> | Landing (light) | Landing (dark) |
> |---|---|
> | `docs/landing-light.png` | `docs/landing-dark.png` |

---

## 📂 Project Structure

```
expense-tracker/
├── app.py                  # Flask app: routes + DB startup (init_db + seed_db)
├── database/
│   ├── __init__.py
│   └── db.py               # Data-access layer: get_db(), init_db(), seed_db()
├── templates/
│   ├── base.html           # Shared layout: navbar, footer, theme toggle, assets
│   ├── landing.html        # Marketing / home page
│   ├── login.html          # Sign in
│   ├── register.html       # Create account
│   ├── terms.html          # Terms & Conditions
│   └── privacy.html        # Privacy Policy
├── static/
│   ├── css/style.css       # All styling (light + dark themes)
│   └── js/main.js          # Theme toggle, video modal
├── requirements.txt
├── expense_tracker.db      # SQLite DB (gitignored — created on first run)
└── CLAUDE.md               # Contributor / build-order guidance
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.9+**
- `pip` and `venv`

### Installation

```bash
# 1. Clone
git clone https://github.com/sankalp10525/Expensio.git
cd Expensio

# 2. Create & activate a virtual environment
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the dev server
python3 app.py
```

The app starts on **http://127.0.0.1:5001** (note: port **5001**, not Flask's default 5000) in
debug mode with auto-reload. The SQLite database is **created and seeded automatically** on first run.

> 💡 The venv doesn't persist across separate shell invocations. Either chain the activation
> (`source venv/bin/activate && python3 app.py`) or call the binary directly (`venv/bin/python3 app.py`).

### Demo Account

The seed data creates a demo user you can use once auth is wired up:

| Email | Password |
|---|---|
| `demo@spendly.com` | `demo123` |

---

## 🗄 Database

The `database/` package is the single data-access layer. `database/db.py` exposes three functions:

| Function | Purpose |
|---|---|
| `get_db()` | Returns a SQLite connection with `row_factory = sqlite3.Row` and `PRAGMA foreign_keys = ON`. |
| `init_db()` | Creates tables using `CREATE TABLE IF NOT EXISTS` (safe to call repeatedly). |
| `seed_db()` | Inserts a demo user + 8 sample expenses. Idempotent — no-ops if data already exists. |

Both `init_db()` and `seed_db()` run automatically at app startup inside an `app.app_context()`.
You can also initialize the DB standalone:

```bash
venv/bin/python3 database/db.py
```

### Schema

**`users`**

| Column | Type | Constraints |
|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `name` | TEXT | NOT NULL |
| `email` | TEXT | UNIQUE, NOT NULL |
| `password_hash` | TEXT | NOT NULL |
| `created_at` | TEXT | DEFAULT `datetime('now')` |

**`expenses`**

| Column | Type | Constraints |
|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `user_id` | INTEGER | NOT NULL, FK → `users(id)` |
| `amount` | REAL | NOT NULL |
| `category` | TEXT | NOT NULL |
| `date` | TEXT | NOT NULL (`YYYY-MM-DD`) |
| `description` | TEXT | nullable |
| `created_at` | TEXT | DEFAULT `datetime('now')` |

**Categories** (fixed list): `Food` · `Transport` · `Bills` · `Health` · `Entertainment` · `Shopping` · `Other`

---

## 🗺 Build Roadmap

Expensio is built in a fixed order. Placeholder routes in `app.py` return `"... coming in Step N"`
until each step is implemented.

| Step | Feature | Status |
|:---:|---|:---:|
| 1 | **Database setup** — `get_db`, `init_db`, `seed_db` | ✅ Done |
| 2 | Registration handler (hash & store user) | 🚧 |
| 3 | Login / logout + sessions | 🚧 |
| 4 | Profile page | 🚧 |
| 5–6 | Dashboard & expense listing | 🚧 |
| 7 | Add expense | 🚧 |
| 8 | Edit expense | 🚧 |
| 9 | Delete expense | 🚧 |

### Routes

| Method | Path | Description |
|---|---|---|
| GET | `/` | Landing page |
| GET | `/register` | Create account form |
| GET | `/login` | Sign in form |
| GET | `/terms` | Terms & Conditions |
| GET | `/privacy` | Privacy Policy |
| GET | `/logout` | _Step 3_ |
| GET | `/profile` | _Step 4_ |
| GET | `/expenses/add` | _Step 7_ |
| GET | `/expenses/<id>/edit` | _Step 8_ |
| GET | `/expenses/<id>/delete` | _Step 9_ |

---

## 📐 Conventions

- **Currency** is Indian Rupees (**₹ / INR**) throughout the UI — never USD.
- All internal links use `url_for('<route_func>')`, so renaming a route function means updating templates too.
- Every page extends `templates/base.html`, which owns the navbar, footer, fonts, theme toggle, and asset links.
- **No ORM** — all SQL is hand-written and **parameterized** (never string-formatted).
- `venv/`, `expense_tracker.db`, `__pycache__/`, and `.env` are gitignored.

---

## 🧪 Testing

Testing is set up with `pytest` and `pytest-flask`:

```bash
venv/bin/pytest                                  # run all tests
venv/bin/pytest path/to/test_file.py::test_name  # run a single test
```

---

## 📜 License

Released under the **MIT License**. See [`LICENSE`](LICENSE) for details.

<div align="center">
<sub>Built with ☕ and ₹ · Expensio</sub>
</div>
