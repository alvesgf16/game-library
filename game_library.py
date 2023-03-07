from flask import Flask, render_template


class Game:
    def __init__(self, a_name: str) -> None:
        self.__name = a_name

    @property
    def name(self) -> str:
        return self.__name


app = Flask(__name__)


@app.route("/start")
def hello() -> str:
    tetris = Game("Tetris")
    skyrim = Game("Skyrim")
    crash = Game("Crash Bandicoot")
    games = [tetris, skyrim, crash]
    return render_template("list.html", a_title="Games", table_data=games)


if __name__ == "__main__":
    app.run()
