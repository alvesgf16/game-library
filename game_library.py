from flask import Flask, render_template


app = Flask(__name__)


@app.route("/start")
def hello():
    return render_template("list.html", a_title="Games")


if __name__ == "__main__":
    app.run()
