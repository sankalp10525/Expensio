# Spec: Login and Logout

## Overview
Add session-based authentication to Expensio. Registration (Step 2) already creates users with
hashed passwords, but there is currently no way to actually sign in — the `/login` route only
renders the form and `/logout` is a placeholder. This step makes login verify a user's email and
password against the `users` table, establish a server-side session identifying the logged-in user,
and lets them log out (clearing that session). The navbar updates to reflect auth state. This is the
foundation every logged-in feature (profile, expense CRUD) depends on.

## Depends on
- **Step 1 — Database setup** (`users` table, `get_db()`).
- **Step 2 — Registration** (users exist with `pbkdf2:sha256` password hashes).

## Routes
- `GET /login` — render the sign-in form — **public**
- `POST /login` — verify credentials; on success set session and redirect to `/profile`, on failure re-render with a generic error — **public**
- `GET /logout` — clear the session and redirect to the landing page — **logged-in** (safe to hit when logged out; simply clears/redirects)

Note: `/profile` remains the Step 4 placeholder — login redirects there, but building the profile page itself is out of scope for Step 3.

## Database changes
No schema changes. The `users` table already has `email` (UNIQUE) and `password_hash`.
A read helper `get_user_by_email(email)` will be added to `database/db.py` (data-access function, not a schema change) so the route stays DB-agnostic.

## Templates
- **Create:** none.
- **Modify:**
  - `templates/login.html` — echo the submitted email back on error (`value="{{ email | default('', true) }}"`) so a failed attempt doesn't wipe the field; password left blank. The existing `{% if error %}` block already renders the message.
  - `templates/base.html` — make the navbar auth-aware: when a user is logged in, show **Profile** and **Logout** links; when logged out, show the existing **Sign in** / **Get started** links. Use the session to decide.

## Files to change
- `app.py` — configure `SECRET_KEY`; import `session`, `redirect`, `url_for`, `check_password_hash`, and `get_user_by_email`; implement `POST /login` (verify + set `session["user_id"]`/`session["user_name"]`) and real `/logout` (`session.clear()`); expose login state to templates (e.g. a `@app.context_processor` providing `current_user`).
- `database/db.py` — add `get_user_by_email(email)` returning the user row or `None`.
- `templates/login.html` — preserve email on error.
- `templates/base.html` — conditional navbar links.

## Files to create
- `tests/test_login.py` — pytest coverage for the login/logout flow (reuses the existing `conftest.py` `app` fixture with an isolated temp DB).

## New dependencies
No new dependencies. `werkzeug.security.check_password_hash` ships with the already-installed Werkzeug; sessions are built into Flask.

## Rules for implementation
- No SQLAlchemy or ORMs.
- Parameterised queries only — never string-format SQL.
- Verify passwords with `werkzeug.security.check_password_hash` (never compare plaintext).
- Do not reveal which field was wrong — use a single generic message: **"Invalid email or password."**
- Normalise the login email with `.strip().lower()` to match how registration stores it.
- `SECRET_KEY` must come from the environment (`os.environ.get("SECRET_KEY", <dev-fallback>)`); `.env` is gitignored. Sessions must not work without a secret key set.
- Use CSS variables — never hardcode hex values (applies to any navbar styling tweaks).
- All templates extend `base.html`.
- Do not auto-login from registration or build the profile page — those belong to their own steps.

## Definition of done
- [ ] Visiting `/login` while logged out renders the form (200).
- [ ] Submitting valid credentials for a seeded/registered user redirects to `/profile` and sets a session cookie.
- [ ] Submitting a wrong password **or** unknown email re-renders `/login` (200) with "Invalid email or password." and no session is set.
- [ ] The submitted email is preserved in the form after a failed attempt; the password field is empty.
- [ ] While logged in, the navbar shows **Profile** and **Logout** (not Sign in / Get started); while logged out it shows Sign in / Get started.
- [ ] `GET /logout` clears the session and redirects to the landing page; afterwards the navbar shows the logged-out links again.
- [ ] Login works end-to-end with the demo user (`demo@expensio.com` / `demo123`).
- [ ] `venv/bin/pytest tests/test_login.py` passes (valid login, bad password, unknown email, logout clears session).
