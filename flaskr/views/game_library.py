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
from flaskr.views.auth import is_user_logged_in, login_required
from flaskr.models import Game
from flaskr.types import Renderable
from flaskr.utils import is_post_request, GameForm, GameCoverUploader

bp = Blueprint("game_library", __name__)


@bp.route("/")
def index() -> str:
    games = list_games()
    return render_template(
        "game_library/index.html",
        a_title="Games",
        table_data=games,
        is_user_logged_in=is_user_logged_in(),
    )


def list_games() -> list[Game]:
    select_all_games = db.select(Game).order_by(Game.name)
    return list(db.session.execute(select_all_games).scalars())


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create() -> Renderable:
    if is_post_request():
        return create_game()
    return render_template(
        "game_library/create.html", a_title="Create a game", form=GameForm()
    )


def create_game() -> Response:
    form = GameForm(request.form)
    return (
        handle_game_creation(form)
        if form.validate_on_submit()
        else redirect(url_for("game_library.create"))
    )


def handle_game_creation(a_form: GameForm) -> Response:
    if is_game_with_name_in_database(a_form.name.data):
        flash("Game already exists!")
    else:
        create_game_from_data(a_form, request)
    return redirect(url_for("game_library.index"))


def is_game_with_name_in_database(a_name: str) -> bool:
    return bool(
        db.session.execute(db.select(Game).filter_by(name=a_name)).scalar()
    )


def create_game_from_data(
    a_form: GameForm, a_request: Request
) -> None:
    game = Game(
        name=a_form.name.data,
        genre=a_form.genre.data,
        platform=a_form.platform.data,
    )
    cover_art = a_request.files["cover-art"]

    add_game_to_database(game)
    GameCoverUploader(game.id).upload_cover_file(cover_art)


def add_game_to_database(a_game: Game) -> None:
    db.session.add(a_game)
    db.session.commit()


@bp.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update(id: int) -> Renderable:
    game = db.session.execute(db.select(Game).filter_by(id=id)).scalar()
    assert isinstance(game, Game)
    form = GameForm()
    form.name.data = game.name
    form.genre.data = game.genre
    form.platform.data = game.platform
    game_cover = GameCoverUploader(id).retrieve_uploaded_cover_filename()
    if request.method == "POST":
        return update_game(game)
    return render_template(
        "game_library/update.html",
        a_title="Updating a game",
        game_id=id,
        form=form,
        game_cover=game_cover,
    )


def update_game(a_game: Game) -> Response:
    form = GameForm(request.form)
    if form.validate_on_submit():
        a_game.name = form.name.data
        a_game.genre = form.genre.data
        a_game.platform = form.platform.data
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
