from flask import Flask, render_template


class Game:
    def __init__(self, a_name: str, a_genre: str, a_platform: str) -> None:
        self.__name = a_name
        self.__genre = a_genre
        self.__platform = a_platform

    @property
    def name(self) -> str:
        return self.__name

    @property
    def genre(self) -> str:
        return self.__genre

    @property
    def platform(self) -> str:
        return self.__platform


app = Flask(__name__)


@app.route("/start")
def hello() -> str:
    tetris = Game("Tetris", "Puzzle", "Atari")
    skyrim = Game("Skyrim", "RPG", "PS3")
    crash = Game("Crash Bandicoot", "Platform", "PS1")
    games = [tetris, skyrim, crash]
    return render_template("list.html", a_title="Games", table_data=games)


if __name__ == "__main__":
    app.run()
