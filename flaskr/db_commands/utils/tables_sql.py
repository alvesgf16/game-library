from typing import Sequence

GAMES_TABLE_NAME = "games"
GAMES_TABLE_CREATION_QUERY = """
CREATE TABLE `games` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(50) NOT NULL,
    `genre` varchar(40) NOT NULL,
    `platform` varchar(20) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
"""
games_table_seeding_query = (
    "INSERT INTO games (name, genre, platform) VALUES (%s, %s, %s)"
)
games_seeding_values = [
    ("Tetris", "Puzzle", "Atari"),
    ("God of War", "Hack 'n' Slash", "PS2"),
    ("Mortal Kombat", "Fighting", "PS2"),
    ("Valorant", "FPS", "PC"),
    ("Crash Bandicoot", "Hack 'n' Slash", "PS2"),
    ("Need for Speed", "Racing", "PS2"),
]
USERS_TABLE_NAME = "users"
USERS_TABLE_CREATION_QUERY = """
CREATE TABLE `users` (
    `name` varchar(20) NOT NULL,
    `username` varchar(10) NOT NULL,
    `password` varchar(100) NOT NULL,
    PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
"""
users_table_seeding_query = (
    "INSERT INTO users (name, username, password) VALUES (%s, %s, %s)"
)
users_seeding_values = [
    ("Gabriel Alves", "alvesgf16", "alohomora"),
    ("Camilla Bastos", "caaaaaams", "paozinho"),
    ("Guilherme Ferreira", "cake", "python_eh_vida"),
]


class Table:
    def __init__(
        self,
        a_name: str,
        a_creation_query: str,
        a_seeding_query: str,
        seeding_values: Sequence[tuple[str, ...]],
    ) -> None:
        self.name = a_name
        self.creation_query = a_creation_query
        self.seeding_query = a_seeding_query
        self.seeding_values = seeding_values


tables = [
    Table(
        USERS_TABLE_NAME,
        USERS_TABLE_CREATION_QUERY,
        users_table_seeding_query,
        users_seeding_values,
    ),
    Table(
        GAMES_TABLE_NAME,
        GAMES_TABLE_CREATION_QUERY,
        games_table_seeding_query,
        games_seeding_values,
    ),
]
