# Spec: Profile Page

## Overview
Build the profile page — the authenticated landing spot Expensio sends users to right after
login (`POST /login` already redirects to `/profile`). Today `/profile` is a placeholder that
returns the string `"Profile page — coming in Step 4"`. This step turns it into a real, login-only
page that shows the signed-in user's account details (name, email, and when they joined) rendered
through a proper template. It also introduces the first authentication guard — a logged-out visitor
hitting `/profile` is bounced to the login page — establishing the pattern every later logged-in
feature (expense CRUD) will reuse. Expense listing and CRUD are out of scope; this page is about the
user's account, not their spending.

## Depends on
- **Step 1 — Database setup** (`users` table with `name`, `email`, `created_at`; `get_db()`).
- **Step 2 — Registration** (real users exist to view).
- **Step 3 — Login and Logout** (session with `user_id`/`user_name`, `current_user` context processor, auth-aware navbar).

## Routes
- `GET /profile` — render the logged-in user's profile; redirect to `/login` if no active session — **logged-in**

No other new routes.

## Database changes
No schema changes. The `users` table already has everything the page needs (`name`, `email`,
`created_at`). A read helper `get_user_by_id(user_id)` will be added to `database/db.py` (a
data-access function, not a schema change) — the session only stores `user_id`/`user_name`, so the
route needs to look up the full row to show the email and join date.

## Templates
- **Create:** `templates/profile.html` — extends `base.html`; overrides `{% block title %}`
  (e.g. "Profile — Expensio") and `{% block content %}`. Displays the user's name, email, and a
  human-readable "Member since" derived from `created_at`. Reuse existing auth/card styling classes
  (`auth-section`, `auth-container`, `auth-card`, etc.) for visual consistency; no new hardcoded
  colours.
- **Modify:** none. The navbar already links to Profile / Logout from Step 3.

## Files to change
- `app.py` — import `get_user_by_id`; replace the placeholder `/profile` route with a real one that
  (a) redirects to `url_for("login")` when `session.get("user_id")` is absent, (b) loads the user via
  `get_user_by_id`, and (c) renders `profile.html` with the user row.
- `database/db.py` — add `get_user_by_id(user_id)` returning the user row or `None`.

## Files to create
- `templates/profile.html` — the profile page template.
- `tests/test_profile.py` — pytest coverage (logged-out redirect, logged-in renders name/email,
  reuses the existing `conftest.py` `app` fixture with an isolated temp DB).

## New dependencies
No new dependencies. Sessions and `render_template` are already in use.

## Rules for implementation
- No SQLAlchemy or ORMs.
- Parameterised queries only — never string-format SQL.
- Passwords hashed with werkzeug (no password is displayed or handled here, but never surface
  `password_hash` in the template).
- The auth guard is a redirect to `login`, not a 403 — match the redirect-based flow already used.
- Use CSS variables — never hardcode hex values.
- All templates extend `base.html`.
- Do not build expense listing, charts, editing the profile, or account settings — this step is
  read-only display of the current user's account.

## Definition of done
- [ ] Visiting `/profile` while logged out redirects to `/login` (302) and does not leak any user data.
- [ ] Logging in as the demo user redirects to `/profile`, which renders (200) showing the user's name and email.
- [ ] The page shows a readable "Member since" value derived from the user's `created_at`.
- [ ] `password_hash` never appears in the rendered HTML.
- [ ] The page extends `base.html` (navbar/footer present) and shows the logged-in navbar (Profile / Logout).
- [ ] Currency, if any amount is ever shown, uses ₹ (no amounts are expected on this page).
- [ ] `venv/bin/pytest tests/test_profile.py` passes (logged-out redirect, logged-in renders name + email).
