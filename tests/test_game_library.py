import unittest

from game_library import app


class TestGameLibrary(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_hello(self):
        response = self.app.get("/start")
        assert response.data == b"<h1>Hello world!</h1>"
