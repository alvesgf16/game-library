from os import environ as env
from types import TracebackType
from typing import Type

import mysql.connector

from mysql.connector.abstracts import MySQLCursorAbstract


class DatabaseOperator:
    def __enter__(self) -> MySQLCursorAbstract:
        self.connection = mysql.connector.connect(
            host="localhost",
            user=env.get("MYSQL_USER"),
            password=env.get("MYSQL_PASSWORD"),
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        self.cursor.close()
        self.connection.close()
