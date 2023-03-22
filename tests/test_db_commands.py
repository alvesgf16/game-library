from unittest.mock import patch

from . import TestBase


class TestDb(TestBase):
    def test_db_create(self):
        command_patch = self.__given_a_patched_command_function("db_create")
        result = self.__when_a_command_is_invoked("db-create")
        self.__then_the_correct_message_is_displayed(result, "created")
        self.__then_the_command_function_is_called(command_patch)

    def __given_a_patched_command_function(self, a_command_func):
        command_patcher = patch(f"flaskr.{a_command_func}")
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
