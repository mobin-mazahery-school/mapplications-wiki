from flask import Flask, send_from_directory
import os
import re

app = Flask(__name__)


@app.route("/", defaults={"path": "index"}, methods=["GET"])
@app.route("/<path:path>", methods=["GET"])
def main(path):
    if os.path.isfile(f"static/{path}.html"):
        tmpd = open(f"static/{path}.html").read()
        if "<html-tags:" in tmpd:
            for _, match in enumerate(re.finditer(r"<html-tags:(.+?)\/>", tmpd, re.MULTILINE), start=1):
                fname = match.groups()[0]
                if os.path.isfile(f"html-tags/{fname}"):
                    tmpd = tmpd.replace(match.group(), open(f"html-tags/{fname}").read())
        return tmpd

if __name__ == "__main__":
    app.run()