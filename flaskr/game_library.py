from typing import Union

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug import Response

from flaskr.db import game_library

bp = Blueprint("game_library", __name__)


@bp.route("/")
def index() -> str:
    return render_template(
        "index.html", a_title="Games", table_data=game_library
    )


@bp.route("/create", methods=["GET", "POST"])
def create() -> Union[Response, str]:
    if request.method == "POST":
        name = request.form["name"]
        genre = request.form["genre"]
        platform = request.form["platform"]
        game_library.create(name, genre, platform)
        return redirect(url_for("game_library.index"))
    if is_user_logged_in():
        return render_template("form.html", a_title="Create a game")
    return redirect(
        url_for("auth.login", origin=url_for("game_library.create"))
    )


def is_user_logged_in() -> bool:
    return (
        "logged_in_user" in session and session["logged_in_user"] is not None
    )
