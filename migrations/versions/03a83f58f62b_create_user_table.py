"""create user table

Revision ID: 03a83f58f62b
Revises:
Create Date: 2023-03-22 19:18:55.415782

"""
from alembic import op
from flask_bcrypt import generate_password_hash
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
        column("password_hash", String),
    )

    op.bulk_insert(
        users_table,
        [
            {
                "name": "Gabriel Alves",
                "username": "alvesgf16",
                "password_hash": generate_password_hash("alohomora").decode(
                    "utf-8"
                ),
            },
            {
                "name": "Camilla Bastos",
                "username": "caaaaaams",
                "password_hash": generate_password_hash("paozinho").decode(
                    "utf-8"
                ),
            },
            {
                "name": "Guilherme Ferreira",
                "username": "cake",
                "password_hash": generate_password_hash(
                    "python_eh_vida"
                ).decode("utf-8"),
            },
        ],
    )


def downgrade():
    op.drop_table("users")
