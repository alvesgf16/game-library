import functools
from typing import Optional

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
from flaskr.models import User
from flaskr.types import IntConverter, Renderable, Route
from flaskr.utils import UserForm

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view: Route) -> Route:
    @functools.wraps(view)
    def wrapped_view(**kwargs: Optional[IntConverter]) -> Renderable:
        return (
            view(**kwargs)
            if is_user_logged_in()
            else redirect(url_for("auth.login", origin=request.path))
        )

    return wrapped_view


def is_user_logged_in() -> bool:
    return "logged_in_user" in session


@bp.route("/login", methods=["GET", "POST"])
def login() -> Renderable:
    if is_post_request():
        return auth()
    return render_template(
        "login.html", a_title="Login", origin=origin(), form=UserForm()
    )


def is_post_request() -> bool:
    return request.method == "POST"


def origin() -> str:
    return request.args.get("origin") or "/"


def auth() -> Response:
    form = UserForm(request.form)
    user = is_there_a_user_with_username(form.username.data)
    if user and user.password_matches(form.password.data):
        return succesful_user_login(user)
    return unsuccesful_user_login(user)


def is_there_a_user_with_username(a_username: str) -> Optional[User]:
    return db.session.execute(
        db.select(User).filter_by(username=a_username)
    ).scalar()


def succesful_user_login(a_user: User) -> Response:
    set_session_user(a_user.username)
    flash(f"{a_user.username} logged in succesfully!")
    return redirect(origin_of_request())


def unsuccesful_user_login(a_user: Optional[User]) -> Response:
    error = "Incorrect username." if a_user is None else "Incorrect password."
    flash(error)
    return redirect(url_for("auth.login"))


def set_session_user(a_username: Optional[str]) -> None:
    session.clear()
    if a_username:
        session["logged_in_user"] = a_username


def origin_of_request() -> str:
    return request.form["origin"]


@bp.route("/logout")
def logout() -> Response:
    set_session_user(None)
    flash("Logout succesful!")
    return redirect(url_for("game_library.index"))
