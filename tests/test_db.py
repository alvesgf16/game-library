from unittest.mock import MagicMock, patch

import mysql.connector
from mysql.connector import errorcode

from . import TestBase


class TestDb(TestBase):
    def setUp(self):
        super().setUp()
        connect_patcher = patch("mysql.connector.connect")
        self.mock_connect = connect_patcher.start()
        self.addCleanup(connect_patcher.stop)

    def test_db_create_succesful(self):
        self.base_success_case_test("db-create", "created")

    def test_db_create_access_denied(self):
        self.__given_a_mocked_connection_error(
            errorcode.ER_ACCESS_DENIED_ERROR
        )
        result = self.__when_a_command_is_invoked("db-create")
        self.__then_the_correct_message_is_displayed(result, "something wrong")

    def test_db_create_table_already_exists(self):
        self.__given_a_mocked_connection_error(errorcode.ER_TABLE_EXISTS_ERROR)
        result = self.__when_a_command_is_invoked("db-create")
        self.__then_the_correct_message_is_displayed(
            result, "Table already exists"
        )

    def test_db_seed_successful(self):
        self.base_success_case_test("db-seed", "seeding complete")

    def test_db_seed_access_denied(self):
        self.__given_a_mocked_connection_error(
            errorcode.ER_ACCESS_DENIED_ERROR
        )
        result = self.__when_a_command_is_invoked("db-seed")
        self.__then_the_correct_message_is_displayed(result, "something wrong")

    def base_success_case_test(self, a_command, expected_text):
        self.__given_a_mocked_database()
        result = self.__when_a_command_is_invoked(a_command)
        self.__then_the_correct_message_is_displayed(result, expected_text)
        assert self.mock_connect.called

    def __given_a_mocked_database(self):
        mock_connection = MagicMock()
        self.mock_connect.return_value = mock_connection

    def __given_a_mocked_connection_error(self, an_error_code):
        self.mock_connect.side_effect = mysql.connector.Error(
            errno=an_error_code
        )

    def __when_a_command_is_invoked(self, a_command):
        return self.runner.invoke(args=[a_command])

    def __then_the_correct_message_is_displayed(self, actual, expected_text):
        assert expected_text in actual.output
