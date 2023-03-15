import click
import mysql.connector
from mysql.connector.abstracts import MySQLCursorAbstract

from flaskr.db_commands.utils import (
    create_exception_message,
    DatabaseOperator,
    Table,
    tables,
)


@click.command("db-seed")
def db_seed_command() -> None:
    db_seed()


def db_seed() -> None:
    try:
        with DatabaseOperator(
            database="game_library", is_transactional=True
        ) as db_operator:
            DatabaseSeeder("game_library", db_operator)
    except mysql.connector.Error as e:
        create_exception_message(e)


class DatabaseSeeder:
    def __init__(
        self, a_database_name: str, a_cursor: MySQLCursorAbstract
    ) -> None:
        self.database = a_database_name
        self.cursor = a_cursor

        self.seed_tables()
        print("Database seeding complete.")

    def seed_tables(self) -> None:
        for table in tables:
            self.seed_table(table)
            self.display_table_values(table.name)

    def seed_table(self, a_table: Table) -> None:
        self.cursor.executemany(a_table.seeding_query, a_table.seeding_values)

    def display_table_values(self, a_table_name: str) -> None:
        print(f" -------------  {a_table_name.capitalize()}:  -------------")
        self.cursor.execute(f"SELECT * FROM {a_table_name}")
        for value in self.cursor.fetchall():
            print(value[1])
