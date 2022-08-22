from flask import Flask, send_from_directory
import os
import re

app = Flask(__name__)


@app.route("/", defaults={"path": "index"}, methods=["GET"])
@app.route("/<path:path>", methods=["GET"])
def main(path):
    print(path)
    if os.path.isfile(f"static/{path}.html"):
        tmpd = open(f"static/{path}.html", "r", encoding="utf-8").read()
        if "<htmltags:" in tmpd:
            for _, match in enumerate(re.finditer(r"<htmltags:(.+?)\/>", tmpd, re.MULTILINE), start=1):
                fname = match.groups()[0]
                if os.path.isfile(f"html-tags/{fname}.html"):
                    tmpd = tmpd.replace(match.group(), open(f"html-tags/{fname}.html", "r", encoding="utf-8").read())
                    print(match.group())
        return tmpd
    else:
        return "Not found"

if __name__ == "__main__":
    app.run()