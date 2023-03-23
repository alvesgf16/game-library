from typing import Union

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug import Request, Response
from werkzeug.datastructures import FileStorage

from flaskr import db
from flaskr.auth.views import login_required
from flaskr.game_library.models import Game

bp = Blueprint("game_library", __name__)


@bp.route("/")
def index() -> str:
    games = db.session.execute(db.select(Game).order_by(Game.name)).scalars()
    return render_template(
        "game_library/index.html", a_title="Games", table_data=games
    )


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create() -> Union[Response, str]:
    if request.method == "POST":
        return create_game()
    return render_template("game_library/create.html", a_title="Create a game")


def create_game() -> Response:
    if is_game_with_name_in_database(request.form["name"]):
        flash("Game already exists!")
    else:
        create_game_from_data(request)
    return redirect(url_for("game_library.index"))


def is_game_with_name_in_database(a_name: str) -> bool:
    return bool(db.session.execute(
        db.select(Game).filter_by(name=a_name)
    ).scalar())


def create_game_from_data(a_request: Request) -> None:
    game = Game(
        name=a_request.form["name"],
        genre=a_request.form["genre"],
        platform=a_request.form["platform"],
    )
    cover_art = a_request.files["cover-art"]

    add_game_to_database(game)
    add_cover_to_uploads(cover_art, game.id)


def add_game_to_database(a_game: Game) -> None:
    db.session.add(a_game)
    db.session.commit()


def add_cover_to_uploads(a_cover_art: FileStorage, a_game_id: int):
    upload_path = current_app.config["UPLOAD_PATH"]
    a_cover_art.save(f"{upload_path}/cover{a_game_id}.jpg")


@bp.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update(id: int) -> Union[Response, str]:
    game = db.session.execute(db.select(Game).filter_by(id=id)).scalar()
    assert isinstance(game, Game)
    if request.method == "POST":
        return update_game(game)
    return render_template(
        "game_library/update.html", a_title="Updating a game", game=game
    )


def update_game(a_game: Game) -> Response:
    a_game.name = request.form["name"]
    a_game.genre = request.form["genre"]
    a_game.platform = request.form["platform"]
    db.session.commit()

    return redirect(url_for("game_library.index"))


@bp.route("/delete/<int:id>")
@login_required
def delete(id: int) -> Response:
    game = db.session.execute(db.select(Game).filter_by(id=id)).scalar()
    db.session.delete(game)
    db.session.commit()
    flash("Game deleted successfully!")
    return redirect(url_for("game_library.index"))
