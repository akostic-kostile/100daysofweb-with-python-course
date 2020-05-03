from flask import render_template
from program import app


@app.route("/")
# @app.route("/index")
def index():
    # return render_template("index.html", title="Template Demo", time=timenow)
    return "Root!"


@app.route("/index")
def index2():
    # return render_template("index.html", title="Template Demo", time=timenow)
    return "Hello from index!"


# @app.route("/100Days")
# def p100days():
#     return render_template("100Days.html")
