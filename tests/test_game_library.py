import io
from unittest.mock import patch

from . import TestBase


class TestGameLibrary(TestBase):
    def setUp(self):
        super().setUp()
        uploader_patcher = patch("werkzeug.datastructures.FileStorage.save")
        uploader_patcher.start()
        self.addCleanup(uploader_patcher.stop)

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
            response, b"<td>Valorant</td>", b"<td>FPS</td>", b"<td>PC</td>"
        )

    def test_create_as_logged_in_user(self):
        self._page_header_for_logged_in_user_test(
            "/create", b"<h1>Create a game</h1>"
        )

    def test_create_as_random_user(self):
        response = self.__when_the_test_client_calls_a_route("/create")
        self.__then_the_page_header_contains_the_correct_text(
            response, b"<h1>Login</h1>"
        )

    def test_game_creation(self):
        self.auth.login()
        response = self.__when_the_test_client_posts_on_a_route(
            "/create",
            {
                "cover-art": (io.BytesIO(b"abcdef"), "test.jpg"),
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

    def test_game_creation_with_missing_data(self):
        self.auth.login()
        response = self.__when_the_test_client_posts_on_a_route(
            "/create",
            {
                "cover-art": (io.BytesIO(b"abcdef"), "test.jpg"),
                "name": "",
                "genre": "",
                "platform": "",
            },
        )
        self.__then_the_page_header_contains_the_correct_text(
                response, b"<h1>Create a game</h1>"
            )

    def test_update_as_logged_in_user(self):
        self._page_header_for_logged_in_user_test(
            "/update/1", b"<h1>Updating a game</h1>"
        )

    def test_update_as_random_user(self):
        response = self.__when_the_test_client_calls_a_route("/update/1")
        self.__then_the_page_header_contains_the_correct_text(
            response, b"<h1>Login</h1>"
        )

    def test_game_update(self):
        self.auth.login()
        response = self.__when_the_test_client_posts_on_a_route(
            "/update/5",
            {
                "cover-art": (io.BytesIO(b"abcdef"), "test.jpg"),
                "name": "Crash Bandicoot",
                "genre": "Platform",
                "platform": "PS1",
            },
        )
        self.__then_the_cells_in_a_table_line_contain_the_correct_data(
            response,
            b"<td>Crash Bandicoot</td>",
            b"<td>Platform</td>",
            b"<td>PS1</td>",
        )

    def test_delete_as_random_user(self):
        response = self.__when_the_test_client_calls_a_route("/delete/1")
        self.__then_the_page_header_contains_the_correct_text(
            response, b"<h1>Login</h1>"
        )

    def test_delete_as_logged_in_user(self):
        self.auth.login()
        response = self.__when_the_test_client_calls_a_route("/delete/6")
        self.__then_the_deleted_game_is_not_in_the_page(response)

    def _page_header_for_logged_in_user_test(self, a_route, header_text):
        self.auth.login()
        response = self.__when_the_test_client_calls_a_route(a_route)
        self.__then_the_page_header_contains_the_correct_text(
            response, header_text
        )

    def __when_the_test_client_calls_a_route(self, route):
        return self.client.get(route, follow_redirects=True)

    def __when_the_test_client_posts_on_a_route(self, route, data):
        return self.client.post(
            route,
            data=data,
            follow_redirects=True,
            content_type="multipart/form-data",
        )

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

    def __then_the_deleted_game_is_not_in_the_page(self, response):
        assert b"<td>Need for Speed</td>" not in response.data

    def __then_the_page_header_contains_the_correct_text(
        self, response, header_text
    ):
        assert header_text in response.data
