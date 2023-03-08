from flask import Flask, render_template, request


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


class Games(list[Game]):
    def __init__(self) -> None:
        self.append(Game("Tetris", "Puzzle", "Atari"))
        self.append(Game("Skyrim", "RPG", "PS3"))
        self.append(Game("Crash Bandicoot", "Platform", "PS1"))


app = Flask(__name__)
games = Games()


@app.route("/")
def index() -> str:
    return render_template("index.html", a_title="Games", table_data=games)


@app.route("/form")
def form() -> str:
    return render_template("form.html", a_title="Create a game")


@app.route("/create", methods=["POST"])
def create() -> str:
    name = request.form["name"]
    genre = request.form["genre"]
    platform = request.form["platform"]
    game = Game(name, genre, platform)
    games.append(game)
    return render_template("index.html", a_title="Games", table_data=games)


if __name__ == "__main__":
    app.run()
