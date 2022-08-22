from flask import Flask, send_from_directory
import os
import re

app = Flask(__name__)


@app.route("/", defaults={"path": "index"}, methods=["GET"])
@app.route("/<path:path>", methods=["GET"])
def main(path):
    return send_from_directory("static", f"{path}.html")

if __name__ == "__main__":
    app.run()