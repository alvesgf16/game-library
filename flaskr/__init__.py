import click
from typing import Optional

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from flaskr.types import TestConfig


db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
bcrypt = Bcrypt()


def create_app(test_config: Optional[TestConfig] = None) -> Flask:
    app = AppInitializer(Flask(__name__))
    app.load_config(test_config)
    return app.init()


class AppInitializer:
    def __init__(self, app: Flask) -> None:
        self.app = app

    def load_config(self, test_config: Optional[TestConfig]) -> None:
        self.app.config.from_pyfile("config.py")
        if test_config is not None:
            self.app.config.update(test_config)

    def init(self) -> Flask:
        db.init_app(self.app)
        migrate.init_app(self.app, db)
        csrf.init_app(self.app)
        bcrypt.init_app(self.app)
        self.__add_cli_commands()
        self.__register_blueprints()
        return self.app

    def __add_cli_commands(self) -> None:
        self.app.cli.add_command(db_create_command)

    def __register_blueprints(self) -> None:
        from .views import auth, game_library

        self.app.register_blueprint(auth)
        self.app.register_blueprint(game_library)


@click.command("db-create")
def db_create_command() -> None:
    click.echo("Connecting...")
    db_create()
    click.echo("Database created.")


def db_create() -> None:
    db.drop_all()
    db.create_all()
