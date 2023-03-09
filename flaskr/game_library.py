from flask import Blueprint, redirect, render_template, request
from werkzeug import Response

from flaskr.db import game_library


bp = Blueprint('game_library', __name__)


@bp.route("/")
def index() -> str:
    return render_template(
        "index.html", a_title="Games", table_data=game_library
    )


@bp.route("/form")
def form() -> str:
    return render_template("form.html", a_title="Create a game")


@bp.route("/create", methods=["POST"])
def create() -> Response:
    name = request.form["name"]
    genre = request.form["genre"]
    platform = request.form["platform"]
    game_library.create(name, genre, platform)
    return redirect("/")


@bp.route("/login")
def login() -> str:
    return render_template("login.html", a_title="Login")


@bp.route("/auth", methods=["POST"])
def auth() -> Response:
    if request.form["password"] == "alohomora":
        return redirect("/")
    else:
        return redirect("/login")
