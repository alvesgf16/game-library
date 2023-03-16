import click

from flaskr import db


@click.command("db-create")
def db_create_command() -> None:
    click.echo("Connecting...")
    db_create()
    click.echo("Database created.")


def db_create() -> None:
    db.drop_all()
    db.create_all()
