from flask import redirect, render_template, request
from werkzeug import Response

from flaskr import create_app
from flaskr.db import game_library


app = create_app()


@app.route("/")
def index() -> str:
    return render_template(
        "index.html", a_title="Games", table_data=game_library
    )


@app.route("/form")
def form() -> str:
    return render_template("form.html", a_title="Create a game")


@app.route("/create", methods=["POST"])
def create() -> Response:
    name = request.form["name"]
    genre = request.form["genre"]
    platform = request.form["platform"]
    game_library.create(name, genre, platform)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
