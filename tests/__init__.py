import unittest

from flaskr import create_app, db, db_create
from flaskr.auth.models import User
from flaskr.game_library.models import Game


class TestBase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        with self.app.app_context():
            db_create()
            db.session.add_all(
                [
                    User(
                        name="Gabriel Alves",
                        username="alvesgf16",
                        password="alohomora",
                    ),
                    User(
                        name="Camilla Bastos",
                        username="caaaaaams",
                        password="paozinho",
                    ),
                    User(
                        name="Guilherme Ferreira",
                        username="cake",
                        password="python_eh_vida",
                    ),
                    Game(name="Tetris", genre="Puzzle", platform="Atari"),
                    Game(
                        name="God of War",
                        genre="Hack 'n' Slash",
                        platform="PS2",
                    ),
                    Game(
                        name="Mortal Kombat", genre="Fighting", platform="PS2"
                    ),
                    Game(name="Valorant", genre="FPS", platform="PC"),
                    Game(
                        name="Crash Bandicoot",
                        genre="Hack 'n' Slash",
                        platform="PS2",
                    ),
                    Game(
                        name="Need for Speed", genre="Racing", platform="PS2"
                    ),
                ]
            )
            db.session.commit()
        self.client = self.app.test_client()
        self.runner = self.app.test_cli_runner()
        self.auth = AuthActions(self.client)

    def _when_the_test_client_calls_a_route(self, route):
        return self.client.get(route, follow_redirects=True)

    def _when_the_test_client_posts_on_a_route(self, route, data):
        return self.client.post(route, data=data, follow_redirects=True)

    def _then_the_page_header_contains_the_correct_text(
        self, response, header_text
    ):
        assert header_text in response.data


class AuthActions:
    def __init__(self, a_client):
        self._client = a_client

    def login(
        self, a_username="alvesgf16", a_password="alohomora", an_origin=""
    ):
        return self._client.post(
            "/auth/login",
            data={
                "username": a_username,
                "password": a_password,
                "origin": an_origin,
            },
            follow_redirects=True,
        )

    def logout(self):
        return self._client.get("/auth/logout")
