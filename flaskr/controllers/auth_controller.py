from typing import Optional

from flask import flash, redirect, request, session, url_for
from werkzeug import Response

from flaskr import db
from flaskr.models import User
from flaskr.utils import UserForm


def is_user_logged_in() -> bool:
    return "logged_in_user" in session


def origin() -> str:
    return request.args.get("origin") or "/"


def auth() -> Response:
    form = UserForm(request.form)
    user = is_there_a_user_with_username(form.username.data)
    if user and user.password_matches(form.password.data):
        return succesful_user_login(user)
    return unsuccesful_user_login(user)


def is_there_a_user_with_username(a_username: str) -> Optional[User]:
    select_user_by_username = db.select(User).filter_by(username=a_username)
    return db.session.execute(select_user_by_username).scalar()


def succesful_user_login(a_user: User) -> Response:
    set_session_user(a_user.username)
    flash(f"{a_user.username} logged in succesfully!")
    return redirect(origin_of_request())


def set_session_user(a_username: Optional[str]) -> None:
    session.clear()
    if a_username:
        session["logged_in_user"] = a_username


def origin_of_request() -> str:
    return request.form["origin"]


def unsuccesful_user_login(a_user: Optional[User]) -> Response:
    error = "Incorrect username." if a_user is None else "Incorrect password."
    flash(error)
    return redirect(url_for("auth.login"))
