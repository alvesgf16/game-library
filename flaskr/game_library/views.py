from typing import Union

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from werkzeug import Request, Response

from flaskr import db
from flaskr.auth.views import is_user_logged_in, login_required
from flaskr.game_library.models import Game
from flaskr.game_library.helpers import GameCoverUploader

bp = Blueprint("game_library", __name__)


@bp.route("/")
def index() -> str:
    games = db.session.execute(db.select(Game).order_by(Game.name)).scalars()
    return render_template(
        "game_library/index.html",
        a_title="Games",
        table_data=games,
        is_user_logged_in=is_user_logged_in(),
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
    return bool(
        db.session.execute(db.select(Game).filter_by(name=a_name)).scalar()
    )


def create_game_from_data(a_request: Request) -> None:
    game = Game(
        name=a_request.form["name"],
        genre=a_request.form["genre"],
        platform=a_request.form["platform"],
    )
    cover_art = a_request.files["cover-art"]

    add_game_to_database(game)
    GameCoverUploader(game.id).upload_cover_file(cover_art)


def add_game_to_database(a_game: Game) -> None:
    db.session.add(a_game)
    db.session.commit()


@bp.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update(id: int) -> Union[Response, str]:
    game = db.session.execute(db.select(Game).filter_by(id=id)).scalar()
    game_cover = GameCoverUploader(id).retrieve_uploaded_cover_filename()
    assert isinstance(game, Game)
    if request.method == "POST":
        return update_game(game)
    return render_template(
        "game_library/update.html",
        a_title="Updating a game",
        game=game,
        game_cover=game_cover,
    )


def update_game(a_game: Game) -> Response:
    a_game.name = request.form["name"]
    a_game.genre = request.form["genre"]
    a_game.platform = request.form["platform"]
    game_cover = request.files["cover-art"]
    db.session.commit()

    cover_file_manager = GameCoverUploader(a_game.id)
    cover_file_manager.delete_cover_file()
    cover_file_manager.upload_cover_file(game_cover)

    return redirect(url_for("game_library.index"))


@bp.route("/delete/<int:id>")
@login_required
def delete(id: int) -> Response:
    game = db.session.execute(db.select(Game).filter_by(id=id)).scalar()
    db.session.delete(game)
    db.session.commit()
    flash("Game deleted successfully!")
    return redirect(url_for("game_library.index"))


@bp.route("/uploads/<filename>")
def image(filename: str) -> Response:
    return send_from_directory("uploads", filename)
