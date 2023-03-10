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


@bp.route("/form")
def form() -> Union[Response, str]:
    if "logged_in_user" not in session or session["logged_in_user"] is None:
        return redirect(
            url_for(
                "auth.login", next_page=url_for("game_library.form")
            )
        )
    return render_template("form.html", a_title="Create a game")


@bp.route("/create", methods=["POST"])
def create() -> Response:
    name = request.form["name"]
    genre = request.form["genre"]
    platform = request.form["platform"]
    game_library.create(name, genre, platform)
    return redirect(url_for("game_library.index"))
