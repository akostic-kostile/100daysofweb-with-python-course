from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def hello_world():
    return redirect(url_for("index"))


@app.route("/index")
def index():
    # dir(request)
    # help(request)
    # type(request)
    return "index"


@app.route("/user/")
@app.route("/user/<username>")
def users(username=None):
    # return f"Hello, {escape(username.title())}, welcome back"
    return render_template("hello.html", name=username, title="hello page")
