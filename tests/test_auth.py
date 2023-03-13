from . import TestBase


class TestAuth(TestBase):
    def test_succesful_login(self):
        self.login_test(
            "alohomora",
            "",
            b"<h1>Games</h1>",
            b"alvesgf16 logged in succesfully!",
        )

    def test_unsuccesful_login(self):
        self.login_test(
            "houston", "", b"<h1>Login</h1>", b"User not logged in."
        )

    def test_succesful_login_from_form_page(self):
        self.login_test(
            "alohomora",
            "create",
            b"<h1>Create a game</h1>",
            b"alvesgf16 logged in succesfully",
        )

    def login_test(
        self, password, origin, redirected_page_header, flashed_message
    ):
        response = self._when_the_test_client_posts_on_a_route(
            "/auth/login",
            {
                "username": "alvesgf16",
                "password": password,
                "origin": origin,
            },
        )
        self._then_the_page_header_contains_the_correct_text(
            response, redirected_page_header
        )
        self.__then_the_correct_message_is_flashed(response, flashed_message)

    def test_logout(self):
        response = self._when_the_test_client_calls_a_route("/auth/logout")
        self._then_the_page_header_contains_the_correct_text(
            response, b"<h1>Games</h1>"
        )
        self.__then_the_correct_message_is_flashed(
            response, b"Logout succesful!"
        )

    def __then_the_correct_message_is_flashed(self, response, message):
        assert message in response.data
