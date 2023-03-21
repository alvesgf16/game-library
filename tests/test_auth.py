from . import TestBase

from flask import session


class TestAuth(TestBase):
    def test_succesful_login(self):
        response = self.auth.login()
        self._then_the_page_header_contains_the_correct_text(
            response, b"<h1>Games</h1>"
        )
        self.__then_the_correct_message_is_flashed(
            response, b"alvesgf16 logged in succesfully!"
        )

    def test_login_with_invalid_username(self):
        response = self.auth.login(a_username="sheldor")
        self._then_the_page_header_contains_the_correct_text(
            response, b"<h1>Login</h1>"
        )
        self.__then_the_correct_message_is_flashed(
            response, b"Incorrect username."
        )

    def test_login_with_invalid_password(self):
        response = self.auth.login(a_password="houston")
        self._then_the_page_header_contains_the_correct_text(
            response, b"<h1>Login</h1>"
        )
        self.__then_the_correct_message_is_flashed(
            response, b"Incorrect password."
        )

    def test_succesful_login_from_form_page(self):
        response = self.auth.login(an_origin="create")
        self._then_the_page_header_contains_the_correct_text(
            response, b"<h1>Create a game</h1>"
        )
        self.__then_the_correct_message_is_flashed(
            response, b"alvesgf16 logged in succesfully"
        )

    def test_logout(self):
        self.auth.login()

        with self.client:
            self.auth.logout()
            assert "logged_in_user" not in session

    def __then_the_correct_message_is_flashed(self, response, message):
        assert message in response.data
