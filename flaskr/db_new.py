from os import environ as env
from types import TracebackType
from typing import Type

import click
import mysql.connector
from mysql.connector import errorcode
from mysql.connector.abstracts import MySQLCursorAbstract

GAMES = "games"
GAMES_TABLE_CREATION_QUERY = """
CREATE TABLE `games` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(50) NOT NULL,
    `genre` varchar(40) NOT NULL,
    `platform` varchar(20) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
"""
USERS = "users"
USERS_TABLE_CREATION_QUERY = """
CREATE TABLE `users` (
    `name` varchar(20) NOT NULL,
    `username` varchar(10) NOT NULL,
    `password` varchar(100) NOT NULL,
    PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
"""


@click.command("db-create")
def db_create_command() -> None:
    print("Connecting...")
    db_create()
    click.echo("Initialized the database.")


def db_create() -> None:
    try:
        with DatabaseOperator() as db_operator:
            DatabaseCreator(db_operator)
    except mysql.connector.Error as e:
        create_exception_message(e)


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


class Table:
    def __init__(self, a_name: str, a_creation_query: str) -> None:
        self.name = a_name
        self.creation_query = a_creation_query


class DatabaseCreator:
    def __init__(self, a_cursor: MySQLCursorAbstract) -> None:
        self.cursor = a_cursor

        self.create_database()
        self.create_tables()

    def create_database(self) -> None:
        self.cursor.execute("DROP DATABASE IF EXISTS `game_library`;")
        self.cursor.execute("CREATE DATABASE `game_library`;")
        self.cursor.execute("USE `game_library`;")

    def create_tables(self) -> None:
        tables = [
            Table(USERS, USERS_TABLE_CREATION_QUERY),
            Table(GAMES, GAMES_TABLE_CREATION_QUERY)
        ]
        for table in tables:
            self.create_table(table)

    def create_table(self, a_table: Table) -> None:
        print(f"Creating table {a_table.name}:", end=" ")
        self.cursor.execute(a_table.creation_query)
        print("OK")


def create_exception_message(an_error: mysql.connector.Error) -> None:
    if an_error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("There is something wrong with the username or password")
    elif an_error.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print("Table already exists")
    else:
        print(an_error)
