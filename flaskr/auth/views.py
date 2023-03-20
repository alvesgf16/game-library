from typing import Optional, Union

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

from flaskr import db
from flaskr.auth.models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login() -> Union[Response, str]:
    if request.method == "POST":
        return auth(request.form["username"])
    return render_template("login.html", a_title="Login", origin=origin())


def origin() -> str:
    return request.args.get("origin") or ""


def auth(a_username: str) -> Response:
    if user := is_there_a_user_with_username(a_username):
        if does_password_match(user.password):
            return succesful_user_login(user.username)
    flash("User not logged in.")
    return redirect(url_for("auth.login"))


def is_there_a_user_with_username(a_username: str) -> Optional[User]:
    return db.session.execute(
        db.select(User).filter_by(username=a_username)
    ).scalar()


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
