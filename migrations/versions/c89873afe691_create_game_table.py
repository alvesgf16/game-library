"""create game table

Revision ID: c89873afe691
Revises: 03a83f58f62b
Create Date: 2023-03-22 20:20:17.613857

"""
from alembic import op
from sqlalchemy import Integer, String
from sqlalchemy.sql import column, table


# revision identifiers, used by Alembic.
revision = "c89873afe691"
down_revision = "03a83f58f62b"
branch_labels = None
depends_on = None


def upgrade():
    games_table = table(
        "games",
        column("id", Integer),
        column("name", String),
        column("genre", String),
        column("platform", String),
    )

    op.bulk_insert(
        games_table,
        [
            {
                "id": 1,
                "name": "Tetris",
                "genre": "Puzzle",
                "platform": "Atari",
            },
            {
                "id": 2,
                "name": "God of War",
                "genre": "Hack 'n' Slash",
                "platform": "PS2",
            },
            {
                "id": 3,
                "name": "Mortal Kombat",
                "genre": "Fighting",
                "platform": "PS2",
            },
            {"id": 4, "name": "Valorant", "genre": "FPS", "platform": "PC"},
            {
                "id": 5,
                "name": "Crash Bandicoot",
                "genre": "Hack 'n' Slash",
                "platform": "PS2",
            },
            {
                "id": 6,
                "name": "Need for Speed",
                "genre": "Racing",
                "platform": "PS2",
            },
        ],
    )


def downgrade():
    op.drop_table("games")
