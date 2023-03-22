import click

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    db.init_app(app)
    add_cli_commands(app)
    register_blueprints(app)

    return app


def add_cli_commands(app: Flask) -> None:
    app.cli.add_command(db_create_command)


def register_blueprints(app: Flask) -> None:
    from . import auth, game_library

    app.register_blueprint(auth.bp)
    app.register_blueprint(game_library.bp)


@click.command("db-create")
def db_create_command() -> None:
    click.echo("Connecting...")
    db_create()
    click.echo("Database created.")


def db_create() -> None:
    db.drop_all()
    db.create_all()
