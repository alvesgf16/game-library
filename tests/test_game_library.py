import unittest

from flaskr import create_app


class TestGameLibrary(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.app = app.test_client()

    def test_page_header(self):
        response = self.__when_the_test_client_calls_the_index_route()
        self.__then_the_page_header_contains_the_correct_text(
            response, b"<h1>Games</h1>"
        )

    def test_table_headers(self):
        response = self.__when_the_test_client_calls_the_index_route()
        self.__then_the_cells_in_a_table_line_contain_the_correct_data(
            response, b"<th>Name</th>", b"<th>Genre</th>", b"<th>Platform</th>"
        )

    def test_table_data(self):
        response = self.__when_the_test_client_calls_the_index_route()
        self.__then_the_cells_in_a_table_line_contain_the_correct_data(
            response, b"<td>Tetris</td>", b"<td>Puzzle</td>", b"<td>Atari</td>"
        )
        self.__then_the_cells_in_a_table_line_contain_the_correct_data(
            response, b"<td>Skyrim</td>", b"<td>PS3</td>", b"<td>RPG</td>"
        )
        self.__then_the_cells_in_a_table_line_contain_the_correct_data(
            response,
            b"<td>Crash Bandicoot</td>",
            b"<td>Platform</td>",
            b"<td>PS1</td>",
        )

    def test_game_creation(self):
        response = self.__when_the_test_client_posts_on_the_create_route()
        self.__then_the_cells_in_a_table_line_contain_the_correct_data(
            response,
            b"<td>League of Legends</td>",
            b"<td>MOBA</td>",
            b"<td>PC</td>",
        )

    def __when_the_test_client_calls_the_index_route(self):
        return self.app.get("/")

    def __when_the_test_client_posts_on_the_create_route(self):
        return self.app.post(
            "/create",
            data={
                "name": "League of Legends",
                "genre": "MOBA",
                "platform": "PC",
            },
            follow_redirects=True
        )

    def __then_the_page_header_contains_the_correct_text(
        self, response, header_text
    ):
        assert header_text in response.data

    def __then_the_cells_in_a_table_line_contain_the_correct_data(
        self,
        response,
        name_cell,
        genre_cell,
        platform_cell,
    ):
        assert name_cell in response.data
        assert genre_cell in response.data
        assert platform_cell in response.data
