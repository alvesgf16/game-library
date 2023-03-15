import click
import mysql.connector
from mysql.connector.abstracts import MySQLCursorAbstract

from flaskr.db_commands.utils import (
    create_exception_message,
    DatabaseOperator,
    Table,
    tables,
)


@click.command("db-create")
def db_create_command() -> None:
    print("Connecting...")
    db_create()


def db_create() -> None:
    try:
        with DatabaseOperator() as db_operator:
            DatabaseCreator("game_library", db_operator)
    except mysql.connector.Error as e:
        create_exception_message(e)


class DatabaseCreator:
    def __init__(
        self, a_database_name: str, a_cursor: MySQLCursorAbstract
    ) -> None:
        self.database = a_database_name
        self.cursor = a_cursor

        self.create_database()
        self.create_tables()
        print("Database created.")

    def create_database(self) -> None:
        self.cursor.execute(f"DROP DATABASE IF EXISTS `{self.database}`;")
        self.cursor.execute(f"CREATE DATABASE `{self.database}`;")
        self.cursor.execute(f"USE `{self.database}`;")

    def create_tables(self) -> None:
        for table in tables:
            self.create_table(table)

    def create_table(self, a_table: Table) -> None:
        print(f"Creating table {a_table.name}:", end=" ")
        self.cursor.execute(a_table.creation_query)
        print("OK")
