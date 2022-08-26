from imp import new_module
import sys
m = sys.modules["database"] = new_module("databse")
m.__file__ = "database.py"
exec("""class Record:
    def __init__(self):
        self.__data = {}
        
    def AddData(self, key, value):
        if key and value:
            self.__data[key] = value
        else:
            raise ValueError("Key/Value can't be null")

    @property
    def Data(self):
        return self.__data

from pymongo import MongoClient
client = MongoClient("mongodb+srv://db_user:Mazahery85@discorddrive-database.qt9tx1u.mongodb.net/?retryWrites=true&w=majority", port=27017)
db = client["MAWiki"]
DDtable = db["Users"]

def ChangeDB(dbname):
    global DDtable
    DDtable = db[dbname]

def Insert(data: Record):
    DDtable.insert_one(data.Data)
    
def Update(selector: dict, updated: dict):
    return DDtable.update_one(selector, updated).modified_count
    
def Export(*args: dict):
    return list(DDtable.find(*args))

def Delete(*args: dict):
    return DDtable.delete_one(*args).deleted_count""", m.__dict__)
()
m = sys.modules["MailTrap"] = new_module("MailTrap")
m.__file__ = "MailTrap.py"
exec("""from smtplib import SMTP, SMTPException
class Email:
    def __init__(self):
        self.mailsender = "verify"
        self.name = f"M-Applications {self.mailsender[0].upper()}{self.mailsender[1:]}"
        self.domain = "m-applications.cf"
        self.sender = f"{self.mailsender}@{self.domain}"
        self.username="api"
        self.password="f0091e303c5446b7728b5a9321b47b3c"
        self.smtpObj: SMTP
        try:
            self.smtpObj = SMTP('send.smtp.mailtrap.io', port=587)
            self.smtpObj.starttls()
            self.smtpObj.login(user=self.username, password=self.password)
        except SMTPException as e:
            raise(SMTPException(e))
        
    def Update(self):
        self.name = f"M-Applications {self.mailsender[0].upper()}{self.mailsender[1:]}"
        self.sender = f"{self.mailsender}@{self.domain}"
        
    def send_email(self, receiver, subject, message):
        message = f\"\"\"From: {self.name} <{self.sender}>
To: You <{receiver}>
Subject: {subject}
{message}
\"\"\"
        self.smtpObj.sendmail(self.sender, [receiver], message)
        return {"succes":True, "message": "Email sent succesfully"}""", m.__dict__)
()

from flask import Flask, request, redirect, render_template, session
import requests
import json
import database
import MailTrap

app = Flask(__name__)
app.config["SECRET_KEY"] = "952480c69b6a96d86b8e38b4485a4529b7c3c0034f81b5e0feeeb0aef234ce49"

@app.route("/signup")
def signup():
    if not "loggedin" in session.keys() or not session["loggedin"]:
        return render_template("Signup.html")
    return redirect("/dashboard")   

@app.route("/login")
def login():
    if not "loggedin" in session.keys() or not session["loggedin"]:
        return render_template("Login.html")
    return redirect("/dashboard")    

@app.route("/signup", methods=["POST"])
def signup_post():
    if "username" in request.form.keys():
        if "password" in request.form.keys():


@app.route("/login", methods=["POST"])
def login_post():
    if "username" in request.form.keys():
        if "password" in request.form.keys():
            username = request.form.get("username")
            password = request.form.get("password")
            userselector = "username"
            if "@" in username:
                userselector = "email"
            database.ChangeDB("Users")
            dataout = database.Export({userselector:username,"password":password})
            if len(dataout) > 0:
                session["loggedin"] = True
                session["email"] = dataout["email"]
                session["username"] = dataout["username"]
                return redirect("/dashboard")
            else:
                return render_template("Login.html", error_msg="نام کاربری یا رمز عبور نامعتبر است!")

@app.route("/download/<name>")
def download_page(name):
    if "loggedin" in session.keys():
        if session["loggedin"]:
            return redirect(f"/download/d/{name}")
    return redirect("/signup")

@app.route("/download/d/MInstagramBot")
def download_MInstagramBot():
    if "loggedin" in session.keys():
        if session["loggedin"]:
            ver = requests.get("https://m-applications.cf/releases/latest_version.txt").content.decode("utf-8")
            verurls = json.loads(requests.get("https://m-applications.cf/releases/version_urls.json").content.decode("utf-8"))
            return f"<center><h1>در حال آماده سازی</h1></center><script>var a = document.createElement('a');a.href='{verurls[ver]}';a.click();</script>"
    return redirect("/")

@app.route("/", defaults={"path": "index"}, methods=["GET"])
@app.route("/<path:path>", methods=["GET"])
def main(path):
    session["loggedin"] = False
    session["username"] = ""
    return render_template(f"{path}.html", loggedin=(session["loggedin"] if ("loggedin" in session.keys()) else False))

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