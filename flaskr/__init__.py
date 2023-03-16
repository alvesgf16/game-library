from os import environ as env
from urllib.parse import quote

from flask import Flask

from . import auth, game_library
from .db_commands import db_create_command, db_seed_command

mysql_user = env.get("MYSQL_USER") or "root"
mysql_password = env.get("MYSQL_PASSWORD") or ""


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = "alura"
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "{DBMS}://{username}:{password}@{server}/{database}".format(
            DBMS="mysql+mysqlconnector",
            username=quote(mysql_user),
            password=quote(mysql_password),
            server="localhost",
            database="game_library",
        )
    )
    app.register_blueprint(auth.bp)
    app.register_blueprint(game_library.bp)
    app.cli.add_command(db_create_command)
    app.cli.add_command(db_seed_command)
    return app
