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
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import requests
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
        
    def attach_logo(self, email_message, fileaddress):
        extra_headers={'Content-ID':'<title_image>'}
        file_attachment = MIMEApplication(requests.get(fileaddress).content)
        file_attachment.add_header(
            "Content-Disposition",
            f"attachment; filename= Logo.png",
        )
        if extra_headers is not None:
            for name, value in extra_headers.items():
                file_attachment.add_header(name, value)
        email_message.attach(file_attachment)
        
    def send_email(self, receiver, subject, message, html_message, logo_url):
        email_message = MIMEMultipart()
        email_message['From'] = f"{self.name} <{self.sender}>"
        email_message['To'] = f"You <{receiver}>"
        email_message['Subject'] = subject
        email_message.attach(MIMEText(html_message, "html", "utf-8"))
        email_message.attach(MIMEText(message, "plain", "utf-8"))
        self.attach_logo(email_message, logo_url)
        email_string = email_message.as_string()
        self.smtpObj.sendmail(self.sender, [receiver], email_string)
        return {"succes":True, "message": "Email sent succesfully"}""", m.__dict__)
()
m = sys.modules["MailTemplate"] = new_module("MailTemplate")
m.__file__ = "mail_template.py"
exec("""import requests
class MailTemplate:
    def __init__(self):
        self.email = ""
        self.username = ""
        self.confirmlink = ""
        self.title_image_url = ""
        
    def GetData(self):
        mail_template = requests.get('https://wiki.m-applications.cf/static/mail.html').content.decode('utf-8')
        change_dict = {'{self.username}':self.username,'{self.confirmlink}':self.confirmlink,'self.title_image_url':self.title_image_url}
        for item in change_dict:
            mail_template = mail_template.replace(item, change_dict[item])
        return mail_template""",m.__dict__)
()

from flask import Flask, request, redirect, render_template, session
import requests
import json
import uuid
import hashlib
import database
import MailTrap
from MailTemplate import MailTemplate

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config["SECRET_KEY"] = "952480c69b6a96d86b8e38b4485a4529b7c3c0034f81b5e0feeeb0aef234ce49"
@app.route("/signup")
def signup():
    if not "loggedin" in session.keys() or not session["loggedin"]:
        return render_template("Signup.html")
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/login")
def login():
    if not "loggedin" in session.keys() or not session["loggedin"]:
        return render_template("Login.html")
    return redirect("/dashboard")

@app.route("/userverify")
def verify_username(username):
    if len(database.Export({"username":username})) <= 0:
        return True
    else:
        return False

@app.route("/signup", methods=["POST"])
def signup_post():
    if "username" in request.form.keys():
        if "email" in request.form.keys():
            if "password" in request.form.keys():
                if "repass" in request.form.keys():
                    username = request.form.get("username")
                    email = request.form.get("email")
                    password = request.form.get("password")
                    repass = request.form.get("repass")
                    if password == repass:
                        hash_object = hashlib.sha256(bytes(password,"utf-8"))
                        password = hash_object.hexdigest()
                        database.ChangeDB("verification")
                        verification_code = str(uuid.uuid4()).replace("-","")
                        userecord=database.Record()
                        userecord.AddData("code", verification_code)
                        userecord.AddData("username", username)
                        userecord.AddData("email",email)
                        userecord.AddData("password",password)
                        database.Insert(userecord)
                        confirmail = MailTrap.Email()
                        mailtmp = MailTemplate()
                        mailtmp.email=email
                        mailtmp.username = username
                        mailtmp.title_image_url="https://wiki.m-applications.cf/static/Logo.png"
                        mailtmp.confirmlink = f"https://wiki.m-applications.cf/email/verification/{verification_code}"
                        confirmail.send_email(email, "M-Applications Verification", "", mailtmp.GetData(), mailtmp.title_image_url)
                        print(f"New verification email sent: ")
                        return render_template("Signup.html", succes_msg="لینک تایید به ایمیل شما ارسال شد.")
                    else:
                        return render_template("Signup.html", error_msg="رمز عبور و تکرار آن با هم برابر نیستند!")

@app.route("/login", methods=["POST"])
def login_post(wtg=""):
    if "username" in request.form.keys():
        if "password" in request.form.keys():
            username = request.form.get("username")
            password = request.form.get("password")
            hash_object = hashlib.sha256(bytes(password,"utf-8"))
            password = hash_object.hexdigest()
            userselector = "username"
            if "@" in username:
                userselector = "email"
            database.ChangeDB("Users")
            dataout = database.Export({userselector:username,"password":password})
            if len(dataout) > 0:
                dataout=dataout[0]
                session["loggedin"] = True
                session["email"] = dataout["email"]
                session["username"] = dataout["username"]
                if not wtg:
                    return redirect("/dashboard")
                else:
                    return redirect(f"/{wtg}")
            else:
                return render_template("Login.html", error_msg="نام کاربری یا رمز عبور نامعتبر است!")

@app.route("/download/<name>")
def download_page(name):
    if "loggedin" in session.keys():
        if session["loggedin"]:
            return redirect(f"/download/d/{name}")
    return redirect(f"/login?wtg=download/{name}")

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
    return render_template(f"{path}.html", loggedin=(session["loggedin"] if ("loggedin" in session.keys()) else False))

#=================================================[EmailVerification]=================================================
@app.route("/email/verification/<code>")
def email_verification(code):
    database.ChangeDB("verification")
    tbldata = database.Export({"code":code})
    if len(tbldata) > 0:
        tbldata=tbldata[0]
        database.ChangeDB("Users")
        userecord = database.Record()
        userecord.AddData("username",tbldata["username"])
        userecord.AddData("password",tbldata["password"])
        userecord.AddData("email",tbldata["email"])
        database.Insert(userecord)
        database.ChangeDB("verification")
        database.Delete({"code":code})
        return render_template("Verification.html", verified=True)
    else:
        return render_template("Verification.html", verified=False)
    
#=================================================[EmailVerification]=================================================
if __name__ == "__main__":
    app.run()