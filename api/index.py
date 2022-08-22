from flask import Flask, send_from_directory, redirect
import requests

app = Flask(__name__)

@app.route("/download/MInstagramBot")
def download():
    ver = requests.get("https://m-applications.cf/releases/latest_version.txt").content.decode("utf-8")
    accesscode = requests.get("https://m-applications.cf/gak.php").content.decode("utf-8")
    return redirect(f"https://m-applications.cf/download.php?version={ver}&k={accesscode}")

@app.route("/", defaults={"path": "index"}, methods=["GET"])
@app.route("/<path:path>", methods=["GET"])
def main(path):
    return send_from_directory("static", f"{path}.html")

if __name__ == "__main__":
    app.run()