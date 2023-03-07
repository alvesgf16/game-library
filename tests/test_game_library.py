import unittest

from game_library import app


class TestGameLibrary(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_page_header(self):
        response = self.app.get("/start")
        assert b"<h1>Games</h1>" in response.data
