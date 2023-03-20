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
from flaskr.game_library.models import Game

bp = Blueprint("game_library", __name__)


@bp.route("/")
def index() -> str:
    games = db.session.execute(db.select(Game).order_by(Game.name)).scalars()
    return render_template(
        "game_library/index.html", a_title="Games", table_data=games
    )


@bp.route("/create", methods=["GET", "POST"])
def create() -> Union[Response, str]:
    if request.method == "POST":
        return create_game()
    return (
        render_template("game_library/create.html", a_title="Create a game")
        if is_user_logged_in()
        else redirect(
            url_for("auth.login", origin=url_for("game_library.create"))
        )
    )


def create_game() -> Response:
    game = Game(
        name=request.form["name"],
        genre=request.form["genre"],
        platform=request.form["platform"],
    )
    if is_game_duplicated(game):
        flash("Game already exists!")
    else:
        add_game_to_database(game)
    return redirect(url_for("game_library.index"))


def is_game_duplicated(a_game: Game) -> Optional[Game]:
    return db.session.execute(
        db.select(Game).filter_by(name=a_game.name)
    ).scalar()


def add_game_to_database(a_game: Game) -> None:
    db.session.add(a_game)
    db.session.commit()


def is_user_logged_in() -> bool:
    return (
        "logged_in_user" in session and session["logged_in_user"] is not None
    )


@bp.route("/update/<int:id>", methods=["GET"])
def update(id: int) -> Union[Response, str]:
    game = db.session.execute(db.select(Game).filter_by(id=id)).scalar()
    assert isinstance(game, Game)
    return (
        render_template(
            "game_library/update.html", a_title="Updating a game", game=game
        )
        if is_user_logged_in()
        else redirect(
            url_for(
                "auth.login", origin=url_for("game_library.update", id=game.id)
            )
        )
    )
