from flask import Blueprint, render_template, request, redirect, session, Flask, url_for
import sqlite3
import os
from werkzeug.utils import secure_filename
from passlib.hash import sha256_crypt

auth = Flask(__name__)
auth.secret_key = os.urandom(24)

auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")


@auth.route("/login")
@auth.route("/", methods=["POST", "GET"])
def login():
    if "user" not in session:
        if request.method == "POST":
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            phno = int(request.form["phno"])
            password = request.form["password"]
            
            try:
                query = "SELECT password FROM users WHERE phno = {a}".format(a=phno)
            
                pwd = (cur.execute(query)).fetchall()
                
                
                if sha256_crypt.verify(password, pwd[0][0]):
                    
                    session["user"] = phno
                    
                    return redirect(url_for("driveMe.book"))
                else:
                    return render_template("Password Incorrect")
            except:
               
                return "<script>alert('invalid credentials'); window.location.replace('\login');</script>"
        else:
                return render_template("login.html")
    else: 
        return redirect(url_for("driveMe.book"))

@auth.route("/logout")
def logout():
    session.pop("user",None)
    return redirect(url_for("auth.login"))

@auth.route("/register", methods=["POST", "GET"])
def register():
    if "user" not in session:
        if request.method == "POST":
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            name = request.form['name']
            phno = request.form['phno']
            password_toBehash= request.form['password']
            password = sha256_crypt.encrypt(password_toBehash)
            email = request.form['email']
            try:
                querry = "INSERT INTO users (phno,name,password,email) VALUES ({a},'{b}','{c}','{d}')".format(
                    a=phno, b=name, c=password, d=email)
                cur.execute(querry)
                conn.commit()
                
                return "<script>window.alert('User Registered sucesssfully!'); window.location.replace('/login');</script>"
            except:
                
                return "<script>window.alert('cannot register the user'); window.location.replace('/register');</script>"
        else:
            return render_template('register.html')
    else:
        return redirect(url_for("auth.login"))
        
