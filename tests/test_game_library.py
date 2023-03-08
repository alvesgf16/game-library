import unittest

from game_library import app


class TestGameLibrary(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_page_header(self):
        response = self.app.get("/start")
        assert b"<h1>Games</h1>" in response.data

    def test_table_data(self):
        response = self.app.get("/start")
        assert b"<td>Tetris</td>" in response.data
        assert b"<td>Puzzle</td>" in response.data
        assert b"<td>Atari</td>" in response.data
        assert b"<td>Skyrim</td>" in response.data
        assert b"<td>RPG</td>" in response.data
        assert b"<td>PS3</td>" in response.data
        assert b"<td>Crash Bandicoot</td>" in response.data
        assert b"<td>Platform</td>" in response.data
        assert b"<td>PS1</td>" in response.data
