from flask import Flask, send_from_directory, redirect, render_template, session
import requests
import json
import database

app = Flask(__name__)

@app.route("/download/<name>")
def download_page(name):
    if "loggedin" in session.keys():
        return redirect(f"/download/d/{name}")
    return render_template("DownloadPage.html", sample_txt="hello world")
    
@app.route("/download/d/MInstagramBot")
def download_MInstagramBot():
    ver = requests.get("https://m-applications.cf/releases/latest_version.txt").content.decode("utf-8")
    verurls = json.loads(requests.get("https://m-applications.cf/releases/version_urls.json").content.decode("utf-8"))
    return f"<center><h1>در حال آماده سازی</h1></center><script>var a = document.createElement('a');a.href='{verurls[ver]}';a.click();</script>"

@app.route("/", defaults={"path": "index"}, methods=["GET"])
@app.route("/<path:path>", methods=["GET"])
def main(path):
    return send_from_directory("static", f"{path}.html")

#=================================================[EmailVerification]=================================================
@app.route("/email/verification/<code>")
def email_verification(code):
    database.ChangeDB("verification")
    if len(database.Export({"code":code})) > 0:
        database.Delete({"code":code})
        return render_template("Verification.html", verified=True)
    else:
        return render_template("Verification.html", verified=False)
    
#=================================================[EmailVerification]=================================================
if __name__ == "__main__":
    app.run()