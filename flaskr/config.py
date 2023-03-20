from os import environ as env
from urllib.parse import quote

SECRET_KEY = "alura"
SQLALCHEMY_DATABASE_URI = (
    "{DBMS}://{username}:{password}@{server}/{database}".format(
        DBMS="mysql+mysqlconnector",
        username=quote(env.get("MYSQL_USER") or "root"),
        password=quote(env.get("MYSQL_PASSWORD") or ""),
        server="localhost",
        database="game_library",
    )
)
