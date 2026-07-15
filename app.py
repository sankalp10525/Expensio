import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash

from database.db import (
    get_db,
    init_db,
    seed_db,
    create_user,
    get_user_by_email,
    get_user_by_id,
)

app = Flask(__name__)

# Session signing key — sourced from the environment (.env is gitignored); the
# dev fallback keeps local runs working without extra setup.
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")

# Ensure the database schema exists and demo data is present before serving.
with app.app_context():
    init_db()
    seed_db()


@app.context_processor
def inject_current_user():
    """Expose the logged-in user (or None) to every template, e.g. the navbar."""
    uid = session.get("user_id")
    current_user = {"id": uid, "name": session.get("user_name")} if uid else None
    return {"current_user": current_user}


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            error = "All fields are required."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."
        else:
            user_id = create_user(name, email, password)
            if user_id is None:
                error = "An account with that email already exists."
            else:
                return redirect(url_for("login"))

        return render_template("register.html", error=error, name=name, email=email)

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = get_user_by_email(email)
        if user is not None and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            return redirect(url_for("profile"))

        # Generic message — never reveal whether the email or the password was wrong.
        return render_template(
            "login.html", error="Invalid email or password.", email=email
        )

    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    # Auth guard: send logged-out visitors to the login page (redirect, not 403).
    if session.get("user_id") is None:
        return redirect(url_for("login"))

    user = get_user_by_id(session["user_id"])
    if user is None:  # stale session referencing a deleted user
        session.clear()
        return redirect(url_for("login"))

    # created_at is stored by SQLite as "YYYY-MM-DD HH:MM:SS"; render it human-readable
    # and compute how many days the account has existed (for the animated badge).
    member_since = "—"
    member_days = 0
    if user["created_at"]:
        try:
            created = datetime.strptime(user["created_at"], "%Y-%m-%d %H:%M:%S")
            member_since = created.strftime("%-d %B %Y")
            member_days = max((datetime.now() - created).days, 0)
        except ValueError:
            member_since = "—"

    # Initials + first name drive the avatar and the client-side greeting.
    parts = user["name"].split()
    if parts:
        initials = (parts[0][0] + (parts[-1][0] if len(parts) > 1 else "")).upper()
        first_name = parts[0]
    else:
        initials, first_name = "?", user["name"]

    return render_template(
        "profile.html",
        user=user,
        member_since=member_since,
        member_days=member_days,
        initials=initials,
        first_name=first_name,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
