import click

from flaskr import db
from flaskr.game_library.models import Game
from flaskr.auth.models import User

seeding_values = [
    User(name="Gabriel Alves", username="alvesgf16", password="alohomora"),
    User(name="Camilla Bastos", username="caaaaaams", password="paozinho"),
    User(
        name="Guilherme Ferreira", username="cake", password="python_eh_vida"
    ),
    Game(name="Tetris", genre="Puzzle", platform="Atari"),
    Game(name="God of War", genre="Hack 'n' Slash", platform="PS2"),
    Game(name="Mortal Kombat", genre="Fighting", platform="PS2"),
    Game(name="Valorant", genre="FPS", platform="PC"),
    Game(name="Crash Bandicoot", genre="Hack 'n' Slash", platform="PS2"),
    Game(name="Need for Speed", genre="Racing", platform="PS2"),
]


@click.command("db-seed")
def db_seed_command() -> None:
    db_seed()
    click.echo("Database seeding complete.")


def db_seed() -> None:
    for value in seeding_values:
        db.session.add(value)
    db.session.commit()
