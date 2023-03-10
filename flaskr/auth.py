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
        username = request.form["username"]
        if username in [user.username for user in users]:
            user = users.get_by_username(username)
            if does_password_match(user.password):
                return succesful_user_login(user.username)
        flash("User not logged in.")
        return redirect(url_for("auth.login"))
    origin = request.args.get("origin") or ""
    return render_template("login.html", a_title="Login", origin=origin)


def does_password_match(a_password: str) -> bool:
    return request.form["password"] == a_password


def succesful_user_login(a_username: str) -> Response:
    set_session_user(a_username)
    flash(f"{a_username} logged in succesfully!")
    return redirect(origin_of_request())


def set_session_user(a_username: Union[str, None]) -> None:
    session["logged_in_user"] = a_username


def origin_of_request() -> str:
    return request.form["origin"]


@bp.route("/logout")
def logout() -> Response:
    set_session_user(None)
    flash("Logout succesful!")
    return redirect(url_for("game_library.index"))
