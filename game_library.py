from flask import Flask, render_template


app = Flask(__name__)


@app.route("/start")
def hello():
    games = ["Tetris", "Skyrim", "Crash Bandicoot"]
    return render_template("list.html", a_title="Games", table_data=games)


if __name__ == "__main__":
    app.run()
