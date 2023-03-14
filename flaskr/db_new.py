from os import environ as env

import click
import mysql.connector
from mysql.connector import errorcode


def db_create() -> None:
    print("Connecting...")
    try:
        with mysql.connector.connect(
            host="localhost",
            user=env.get("MYSQL_USER"),
            password=env.get("MYSQL_PASSWORD"),
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute("DROP DATABASE IF EXISTS `game_library`;")
                cursor.execute("CREATE DATABASE `game_library`;")
                cursor.execute("USE `game_library`;")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("There is something wrong with the username or password")
        else:
            print(err)


@click.command("db-create")
def db_create_command() -> None:
    db_create()
    click.echo("Initialized the database.")
