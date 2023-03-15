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


class Table:
    def __init__(self, a_name: str, a_creation_query: str) -> None:
        self.name = a_name
        self.creation_query = a_creation_query


tables = [
    Table(USERS, USERS_TABLE_CREATION_QUERY),
    Table(GAMES, GAMES_TABLE_CREATION_QUERY),
]
