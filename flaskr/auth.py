from typing import Union

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug import Response

from flaskr.db import users

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login() -> Union[Response, str]:
    if request.method == "POST":
        if request.form["username"] in [user.username for user in users]:
            user = users.get_by_username(request.form["username"])
            if request.form["password"] == user.password:
                session["logged_in_user"] = user.username
                flash(f"{user.username} logged in succesfully!")
                next_page = request.form["next_page"]
                return redirect(next_page)
            else:
                flash("User not logged in.")
                return redirect(url_for("auth.login"))
        else:
            flash("User not logged in.")
            return redirect(url_for("auth.login"))
    next_page = request.args.get("next_page") or ""
    return render_template("login.html", a_title="Login", next_page=next_page)


@bp.route("/logout")
def logout() -> Response:
    session["logged_in_user"] = None
    flash("Logout succesful!")
    return redirect(url_for("game_library.index"))
