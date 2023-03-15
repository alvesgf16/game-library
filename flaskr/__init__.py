from flask import Flask

from . import auth, game_library
from .db_commands import db_create_command


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = "alura"
    app.register_blueprint(auth.bp)
    app.register_blueprint(game_library.bp)
    app.cli.add_command(db_create_command)
    return app
