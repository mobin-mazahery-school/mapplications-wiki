from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route("/", defaults={"path": ""}, methods=["GET"])
@app.route("/<path:path>", methods=["GET"])
def main(path):
    print(path)
    if len(path) <= 0:
        path = "index.html"
    if os.path.isfile(path):
        return open(f"static/{path}","r").read()