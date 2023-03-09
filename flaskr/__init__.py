from flask import Flask

from . import game_library


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = "alura"
    app.register_blueprint(game_library.bp)
    return app
