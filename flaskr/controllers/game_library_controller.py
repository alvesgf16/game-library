from typing import Optional

from flask import flash, redirect, request, url_for
from werkzeug import Request, Response

from flaskr import db
from flaskr.models import Game
from flaskr.utils import GameForm, GameCoverUploader


def list_games() -> list[Game]:
    select_all_games = db.select(Game).order_by(Game.name)
    return list(db.session.execute(select_all_games).scalars())


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
    select_game_by_name = db.select(Game).filter_by(name=a_name)
    return bool(db.session.execute(select_game_by_name).scalar())


def create_game_from_data(a_form: GameForm, a_request: Request) -> None:
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


def get_game_by_id(an_id: int) -> Optional[Game]:
    select_game_by_id = db.select(Game).filter_by(id=an_id)
    return db.session.execute(select_game_by_id).scalar()


def update_game(a_game: Game) -> Response:
    form = GameForm(request.form)
    if form.validate_on_submit():
        update_game_from_form(a_game, form)
        update_game_cover(a_game)
    return redirect(url_for("game_library.index"))


def update_game_from_form(a_game: Game, a_form: GameForm) -> None:
    a_game.name = a_form.name.data
    a_game.genre = a_form.genre.data
    a_game.platform = a_form.platform.data
    db.session.commit()


def update_game_cover(a_game: Game) -> None:
    game_cover = request.files["cover-art"]
    cover_file_manager = GameCoverUploader(a_game.id)
    cover_file_manager.update_cover_file(game_cover)


def delete_game_from_database(a_game: Optional[Game]) -> None:
    db.session.delete(a_game)
    db.session.commit()
