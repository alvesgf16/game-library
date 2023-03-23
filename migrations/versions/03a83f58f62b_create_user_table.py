"""create user table

Revision ID: 03a83f58f62b
Revises:
Create Date: 2023-03-22 19:18:55.415782

"""
from alembic import op
from sqlalchemy import String
from sqlalchemy.sql import column, table


# revision identifiers, used by Alembic.
revision = "03a83f58f62b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    users_table = table(
        "users",
        column("username", String),
        column("name", String),
        column("password", String),
    )

    op.bulk_insert(
        users_table,
        [
            {
                "name": "Gabriel Alves",
                "username": "alvesgf16",
                "password": "alohomora",
            },
            {
                "name": "Camilla Bastos",
                "username": "caaaaaams",
                "password": "paozinho",
            },
            {
                "name": "Guilherme Ferreira",
                "username": "cake",
                "password": "python_eh_vida",
            },
        ],
    )


def downgrade():
    op.drop_table("users")
