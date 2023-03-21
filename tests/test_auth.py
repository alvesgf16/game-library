from . import TestBase

from flask import session


class TestAuth(TestBase):
    def test_succesful_login(self):
        response = self.auth.login()
        self.__then_the_user_is_redirected_to_the_correct_page(response, "/")
        self.__then_the_correct_message_is_flashed(
            response, "logged in succesfully!"
        )

    def test_login_with_invalid_username(self):
        response = self.auth.login(a_username="sheldor")
        self.__then_the_user_is_redirected_to_the_correct_page(
            response, "/auth/login"
        )
        self.__then_the_correct_message_is_flashed(
            response, "Incorrect username."
        )

    def test_login_with_invalid_password(self):
        response = self.auth.login(a_password="houston")
        self.__then_the_user_is_redirected_to_the_correct_page(
            response, "/auth/login"
        )
        self.__then_the_correct_message_is_flashed(
            response, "Incorrect password."
        )

    def test_succesful_login_from_form_page(self):
        response = self.auth.login(an_origin="create")
        self.__then_the_user_is_redirected_to_the_correct_page(
            response, "/create"
        )
        self.__then_the_correct_message_is_flashed(
            response, "logged in succesfully"
        )

    def test_logout(self):
        self.auth.login()

        with self.client:
            self.auth.logout()
            assert "logged_in_user" not in session

    def __then_the_user_is_redirected_to_the_correct_page(
        self, response, a_path
    ):
        assert response.request.path == a_path

    def __then_the_correct_message_is_flashed(self, response, message):
        assert message in response.text
