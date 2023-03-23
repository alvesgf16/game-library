from os import environ as env, path
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
UPLOAD_PATH = f"{path.dirname(path.abspath(__file__))}/uploads"
