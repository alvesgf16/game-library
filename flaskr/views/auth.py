from flask import Blueprint, flash, redirect, render_template, url_for
from werkzeug import Response

from flaskr.controllers.auth_controller import auth, origin, set_session_user
from flaskr.utils import is_post_request, UserForm
from flaskr.views.types import Renderable

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login() -> Renderable:
    if is_post_request():
        return auth()
    return render_template(
        "login.html", a_title="Login", origin=origin(), form=UserForm()
    )


@bp.route("/logout")
def logout() -> Response:
    set_session_user(None)
    flash("Logout succesful!")
    return redirect(url_for("game_library.index"))
