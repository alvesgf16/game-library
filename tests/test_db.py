from unittest.mock import MagicMock, patch

import mysql.connector
from mysql.connector import errorcode

from . import TestBase


class TestDb(TestBase):
    def test_db_create_succesful(self):
        with patch("mysql.connector.connect") as mock_connect:
            mock_connection = MagicMock()
            mock_connect.return_value = mock_connection
            result = self.runner.invoke(args=["db-create"])
            assert "created" in result.output
            assert mock_connect.called

    def test_db_create_access_denied(self):
        with patch("mysql.connector.connect") as mock_connect:
            mock_connect.side_effect = mysql.connector.Error(
                errno=errorcode.ER_ACCESS_DENIED_ERROR
            )
            result = self.runner.invoke(args=["db-create"])
            assert "something wrong" in result.output

    def test_db_create_table_already_exists(self):
        with patch("mysql.connector.connect") as mock_connect:
            mock_connect.side_effect = mysql.connector.Error(
                errno=errorcode.ER_TABLE_EXISTS_ERROR
            )
            result = self.runner.invoke(args=["db-create"])
            assert "Table already exists" in result.output

    def test_db_seed_successful(self):
        with patch("mysql.connector.connect") as mock_connect:
            mock_connection = MagicMock()
            mock_connect.return_value = mock_connection
            result = self.runner.invoke(args=["db-seed"])
            assert "seeding complete" in result.output
            assert mock_connect.called

    def test_db_seed_access_denied(self):
        with patch("mysql.connector.connect") as mock_connect:
            mock_connect.side_effect = mysql.connector.Error(
                errno=errorcode.ER_ACCESS_DENIED_ERROR
            )
            result = self.runner.invoke(args=["db-seed"])
            assert "something wrong" in result.output
