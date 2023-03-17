from unittest.mock import patch

from . import TestBase


class TestDb(TestBase):
    def test_db_create(self):
        self.base_db_command_test("db_create", "db-create", "created")

    def test_db_seed(self):
        self.base_db_command_test("db_seed", "db-seed", "seeding complete")

    def base_db_command_test(self, a_command_func, a_command, expected_text):
        with self.app.app_context():
            self.__given_a_mocked_command_function(a_command_func)
            result = self.__when_a_command_is_invoked(a_command)
            self.__then_the_correct_message_is_displayed(result, expected_text)

    def __given_a_mocked_command_function(self, a_command_func):
        patch(f"flaskr.db_commands.{a_command_func}.{a_command_func}")

    def __when_a_command_is_invoked(self, a_command):
        return self.runner.invoke(args=[a_command])

    def __then_the_correct_message_is_displayed(self, actual, expected_text):
        assert expected_text in actual.output
