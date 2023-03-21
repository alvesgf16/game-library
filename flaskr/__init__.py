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
    from .db_commands import (
        db_create_command,
        db_drop_command,
        db_seed_command,
    )

    app.cli.add_command(db_create_command)
    app.cli.add_command(db_drop_command)
    app.cli.add_command(db_seed_command)


def register_blueprints(app: Flask) -> None:
    from . import auth, game_library

    app.register_blueprint(auth.bp)
    app.register_blueprint(game_library.bp)
