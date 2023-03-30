from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    send_from_directory,
    url_for,
)
from werkzeug import Response

from flaskr.controllers.game_library_controller import (
    list_games,
    create_game,
    get_game_by_id,
    update_game,
    delete_game_from_database,
)
from flaskr.controllers.auth_controller import is_user_logged_in
from flaskr.types import Game, Renderable
from flaskr.utils import is_post_request, GameCoverUploader, GameForm
from flaskr.utils.decorators import login_required

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


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create() -> Renderable:
    if is_post_request():
        return create_game()
    return render_template(
        "game_library/create.html", a_title="Create a game", form=GameForm()
    )


@bp.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update(id: int) -> Renderable:
    game = get_game_by_id(id)
    assert isinstance(game, Game)
    return (
        update_game(game)
        if is_post_request()
        else render_game_update_template(game)
    )


def render_game_update_template(a_game: Game) -> str:
    form = create_game_form_from_game(a_game)
    game_cover = GameCoverUploader(
        a_game.id
    ).retrieve_uploaded_cover_filename()
    return render_template(
        "game_library/update.html",
        a_title="Updating a game",
        game_id=a_game.id,
        form=form,
        game_cover=game_cover,
    )


def create_game_form_from_game(a_game: Game) -> GameForm:
    result = GameForm()
    result.name.data = a_game.name
    result.genre.data = a_game.genre
    result.platform.data = a_game.platform
    return result


@bp.route("/delete/<int:id>")
@login_required
def delete(id: int) -> Response:
    game = get_game_by_id(id)
    delete_game_from_database(game)
    flash("Game deleted successfully!")
    return redirect(url_for("game_library.index"))


@bp.route("/uploads/<filename>")
def image(filename: str) -> Response:
    return send_from_directory("uploads", filename)
