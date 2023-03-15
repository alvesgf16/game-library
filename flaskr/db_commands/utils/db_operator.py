from os import environ as env
from types import TracebackType
from typing import Type

import mysql.connector

from mysql.connector.abstracts import MySQLCursorAbstract


class DatabaseOperator:
    def __init__(
        self, database: str = "", is_transactional: bool = False
    ) -> None:
        self.database = database
        self.is_transactional = is_transactional

    def __enter__(self) -> MySQLCursorAbstract:
        self.connection = mysql.connector.connect(
            host="localhost",
            user=env.get("MYSQL_USER"),
            password=env.get("MYSQL_PASSWORD"),
            database=self.database,
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        if self.is_transactional:
            self.connection.commit()
        self.cursor.close()
        self.connection.close()
