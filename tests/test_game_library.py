import unittest

from flaskr import create_app


class TestGameLibrary(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.app = app.test_client()

    def test_page_header(self):
        response = self.__when_the_test_client_calls_a_route("/")
        self.__then_the_page_header_contains_the_correct_text(
            response, b"<h1>Games</h1>"
        )

    def test_table_headers(self):
        response = self.__when_the_test_client_calls_a_route("/")
        self.__then_the_cells_in_a_table_line_contain_the_correct_data(
            response, b"<th>Name</th>", b"<th>Genre</th>", b"<th>Platform</th>"
        )

    def test_table_data(self):
        response = self.__when_the_test_client_calls_a_route("/")
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
        response = self.__when_the_test_client_posts_on_a_route(
            "/create",
            {
                "name": "League of Legends",
                "genre": "MOBA",
                "platform": "PC",
            },
        )
        self.__then_the_cells_in_a_table_line_contain_the_correct_data(
            response,
            b"<td>League of Legends</td>",
            b"<td>MOBA</td>",
            b"<td>PC</td>",
        )

    def test_succesful_login(self):
        self.login_test(
            "alohomora", b"<h1>Games</h1>", b"alvesgf16 logged in succesfully!"
        )

    def test_unsuccesful_login(self):
        self.login_test("houston", b"<h1>Login</h1>", b"User not logged in.")

    def login_test(self, password, redirected_page_header, flashed_message):
        response = self.__when_the_test_client_posts_on_a_route(
            "/auth", {"username": "alvesgf16", "password": password}
        )
        self.__then_the_page_header_contains_the_correct_text(
            response, redirected_page_header
        )
        self.__then_the_correct_message_is_flashed(response, flashed_message)

    def __when_the_test_client_calls_a_route(self, route):
        return self.app.get(route)

    def __when_the_test_client_posts_on_a_route(self, route, data):
        return self.app.post(route, data=data, follow_redirects=True)

    def __then_the_correct_message_is_flashed(self, response, message):
        assert message in response.data

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
