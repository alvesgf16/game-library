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

from flaskr.db_old import db_old

bp = Blueprint("game_library", __name__)


@bp.route("/")
def index() -> str:
    return render_template(
        "index.html", a_title="Games", table_data=db_old.games
    )


@bp.route("/create", methods=["GET", "POST"])
def create() -> Union[Response, str]:
    if request.method == "POST":
        return create_game()
    return (
        render_template("form.html", a_title="Create a game")
        if is_user_logged_in()
        else redirect(
            url_for("auth.login", origin=url_for("game_library.create"))
        )
    )


def create_game() -> Response:
    name = request.form["name"]
    genre = request.form["genre"]
    platform = request.form["platform"]
    db_old.games.create(name, genre, platform)
    return redirect(url_for("game_library.index"))


def is_user_logged_in() -> bool:
    return (
        "logged_in_user" in session and session["logged_in_user"] is not None
    )
