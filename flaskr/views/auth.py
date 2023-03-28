import functools
from typing import Callable, Optional, Union

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
from flaskr.utils import UserForm

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(
    view: Callable[..., Union[Response, str]]
) -> Callable[..., Union[Response, str]]:
    @functools.wraps(view)
    def wrapped_view(
        **kwargs: Optional[dict[str, int]]
    ) -> Union[Response, str]:
        return (
            view(**kwargs)
            if is_user_logged_in()
            else redirect(url_for("auth.login", origin=request.path))
        )

    return wrapped_view


def is_user_logged_in() -> bool:
    return "logged_in_user" in session


@bp.route("/login", methods=["GET", "POST"])
def login() -> Union[Response, str]:
    if is_post_request():
        return auth()
    return render_template(
        "login.html", a_title="Login", origin=origin(), form=user_form()
    )


def is_post_request() -> bool:
    return request.method == "POST"


def user_form(form_data: Optional[dict[str, str]] = None) -> UserForm:
    return UserForm(form_data)


def origin() -> str:
    return request.args.get("origin") or "/"


def auth() -> Response:
    form = user_form(request.form)
    user = is_there_a_user_with_username(form.username.data)
    if user is None:
        flash("Incorrect username.")
    elif form.password.data != user.password:
        flash("Incorrect password.")
    else:
        return succesful_user_login(user.username)
    return redirect(url_for("auth.login"))


def is_there_a_user_with_username(a_username: str) -> Optional[User]:
    return db.session.execute(
        db.select(User).filter_by(username=a_username)
    ).scalar()


def succesful_user_login(a_username: str) -> Response:
    set_session_user(a_username)
    flash(f"{a_username} logged in succesfully!")
    return redirect(origin_of_request())


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
