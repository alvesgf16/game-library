from unittest.mock import patch

from . import TestBase


class TestDb(TestBase):
    def test_db_create(self):
        self.base_db_command_test("db-create", "created")

    def test_db_drop(self):
        self.base_db_command_test("db-drop", "dropped")

    def test_db_seed(self):
        self.base_db_command_test("db-seed", "seeding complete")

    def base_db_command_test(self, a_command, expected_text):
        command_patch = self.__given_a_patched_command_function(
            a_command.replace("-", "_")
        )
        result = self.__when_a_command_is_invoked(a_command)
        self.__then_the_correct_message_is_displayed(result, expected_text)
        self.__then_the_command_function_is_called(command_patch)

    def __given_a_patched_command_function(self, a_command_func):
        command_patcher = patch(
            f"flaskr.db_commands.{a_command_func}"
        )
        mock_command = command_patcher.start()
        return command_patcher, mock_command

    def __when_a_command_is_invoked(self, a_command):
        return self.runner.invoke(args=[a_command])

    def __then_the_correct_message_is_displayed(self, actual, expected_text):
        assert expected_text in actual.output

    def __then_the_command_function_is_called(self, a_command_patch):
        command_patcher, mock_command = a_command_patch
        assert mock_command.called
        command_patcher.stop()
