from typing import Union

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug import Response

from flaskr.db import game_library, users


bp = Blueprint("game_library", __name__)


@bp.route("/")
def index() -> str:
    return render_template(
        "index.html", a_title="Games", table_data=game_library
    )


@bp.route("/form")
def form() -> Union[Response, str]:
    if "logged_in_user" not in session or session["logged_in_user"] is None:
        return redirect(
            url_for(
                "game_library.login", next_page=url_for("game_library.form")
            )
        )
    return render_template("form.html", a_title="Create a game")


@bp.route("/create", methods=["POST"])
def create() -> Response:
    name = request.form["name"]
    genre = request.form["genre"]
    platform = request.form["platform"]
    game_library.create(name, genre, platform)
    return redirect(url_for("game_library.index"))


@bp.route("/login")
def login() -> str:
    next_page = request.args.get("next_page") or ""
    return render_template("login.html", a_title="Login", next_page=next_page)


@bp.route("/auth", methods=["POST"])
def auth() -> Response:
    if request.form["username"] in [user.username for user in users]:
        user = users.get_by_username(request.form["username"])
        if request.form["password"] == user.password:
            session["logged_in_user"] = user.username
            flash(f"{user.username} logged in succesfully!")
            next_page = request.form["next_page"]
            return redirect(next_page)
        else:
            flash("User not logged in.")
            return redirect(url_for("game_library.login"))
    else:
        flash("User not logged in.")
        return redirect(url_for("game_library.login"))


@bp.route("/logout")
def logout() -> Response:
    session["logged_in_user"] = None
    flash("Logout succesful!")
    return redirect(url_for("game_library.index"))
