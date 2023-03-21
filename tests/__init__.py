import unittest

from flaskr import create_app


class TestBase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.runner = self.app.test_cli_runner()
        self.auth = AuthActions(self.client)
        self.runner.invoke(args=["db-create"])
        self.runner.invoke(args=["db-seed"])

    def tearDown(self):
        self.runner.invoke(args=["db-drop"])

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
