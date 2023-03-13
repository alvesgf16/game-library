from . import TestBase


class TestGameLibrary(TestBase):
    def test_page_header(self):
        response = self._when_the_test_client_calls_a_route("/")
        self._then_the_page_header_contains_the_correct_text(
            response, b"<h1>Games</h1>"
        )

    def test_table_headers(self):
        response = self._when_the_test_client_calls_a_route("/")
        self.__then_the_cells_in_a_table_line_contain_the_correct_data(
            response, b"<th>Name</th>", b"<th>Genre</th>", b"<th>Platform</th>"
        )

    def test_table_data(self):
        response = self._when_the_test_client_calls_a_route("/")
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

    def test_form_as_logged_in_user(self):
        self.given_a_logged_in_user()
        response = self._when_the_test_client_calls_a_route("/create")
        self._then_the_page_header_contains_the_correct_text(
            response, b"<h1>Create a game</h1>"
        )

    def test_form_as_random_user(self):
        response = self._when_the_test_client_calls_a_route("/create")
        self._then_the_page_header_contains_the_correct_text(
            response, b"<h1>Login</h1>"
        )

    def test_game_creation(self):
        response = self._when_the_test_client_posts_on_a_route(
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

    def given_a_logged_in_user(self):
        with self.app.session_transaction() as mock_session:
            mock_session["logged_in_user"] = "a_user"

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
