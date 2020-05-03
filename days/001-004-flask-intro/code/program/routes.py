import time
from flask import render_template
from program import app # noqa

timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


@app.route("/")
# @app.route("/index")
def root():
    # return render_template("index.html", title="Template Demo", time=timenow)
    return "Root!"


@app.route("/index")
def index():
    return render_template("index.html", title="Template Demo", time=timenow)
    # return render_template("index.html", title="Template Demo")
    # return "Hello from index!"


@app.route("/100Days")
def p100days():
    return render_template("100Days.html", title="100 days page")
