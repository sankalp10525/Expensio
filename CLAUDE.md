# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Expensio is a personal expense-tracker web app (Flask + SQLite + Jinja templates), but the repo is a **step-by-step teaching scaffold**, not a finished application. Most functionality is intentionally left unimplemented for a student to build in a fixed order. Preserve this structure: when asked to implement a feature, fill in the designated placeholder rather than rewriting the scaffold or pulling steps forward.

The intended build order is encoded in the code itself:
- `app.py` — placeholder routes each return a `"... coming in Step N"` string (logout=Step 3, profile=Step 4, add expense=Step 7, edit=Step 8, delete=Step 9).
- `database/db.py` — currently only a spec comment. Step 1 is to implement `get_db()` (SQLite connection with `row_factory` + foreign keys enabled), `init_db()` (`CREATE TABLE IF NOT EXISTS`), and `seed_db()` (sample dev data).
- `static/js/main.js` — empty placeholder for client-side JS added as features are built.

## Commands

All Python commands require the venv, whose activation does **not** persist between separate shell invocations — chain it or call the venv binary directly:

```bash
source venv/bin/activate && python3 app.py     # run dev server on http://127.0.0.1:5001
venv/bin/python3 app.py                         # equivalent, no activation

source venv/bin/activate && pip install -r requirements.txt   # install deps
venv/bin/pytest                                 # run tests (pytest-flask is set up; no tests exist yet)
venv/bin/pytest path/to/test_file.py::test_name # run a single test
```

The app runs in debug mode (auto-reload on save), on port **5001** (not the Flask default 5000).

## Architecture

- **Routing/rendering**: single `app.py` maps routes to `render_template(...)`. All internal links use `url_for('<route_func>')`, so renaming a route function requires updating templates too.
- **Templates**: Jinja inheritance. Every page extends `templates/base.html`, which owns the navbar, footer, Google Fonts, the `style.css` link, and `main.js`. Child pages override `{% block title %}` and `{% block content %}` (also available: `{% block head %}`, `{% block scripts %}`). The brand name "Expensio" appears in `base.html` (title/nav/footer) and per-page titles/copy across the auth and landing templates.
- **Database**: SQLite. The DB file is `expense_tracker.db` (gitignored) — created/seeded by the `init_db()`/`seed_db()` functions once implemented in `database/db.py`. The `database/` package is the single data-access layer.
- **Static assets**: `static/css/style.css` (all styling; hand-written, no framework) and `static/js/main.js`.

## Conventions

- Currency throughout the UI is Indian Rupees (₹).
- No README, no linter config, and no CI. `venv/`, `expense_tracker.db`, `__pycache__/`, and `.env` are gitignored.
