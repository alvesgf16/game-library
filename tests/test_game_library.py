import unittest
from unittest.mock import patch

from game_library import app


class TestGameLibrary(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @patch("game_library.render_template")
    def test_hello(self, mock_render):
        mock_render.return_value = "<h1>Hello world!</h1>"
        response = self.app.get("/start")
        assert response.data == b"<h1>Hello world!</h1>"
