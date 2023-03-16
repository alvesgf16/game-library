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
from flaskr.db_new import Games

bp = Blueprint("game_library", __name__)


@bp.route("/")
def index() -> str:
    games = db.session.execute(db.select(Games).order_by(Games.name)).scalars()
    return render_template("index.html", a_title="Games", table_data=games)


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
    game = Games(
        name=request.form["name"],
        genre=request.form["genre"],
        platform=request.form["platform"],
    )
    if is_game_duplicated(game):
        flash("Game already exists!")
    else:
        add_game_to_database(game)
    return redirect(url_for("game_library.index"))


def is_game_duplicated(a_game: Games) -> Optional[Games]:
    return db.session.execute(
        db.select(Games).filter_by(name=a_game.name)
    ).scalar()


def add_game_to_database(a_game: Games) -> None:
    db.session.add(a_game)
    db.session.commit()


def is_user_logged_in() -> bool:
    return (
        "logged_in_user" in session and session["logged_in_user"] is not None
    )
