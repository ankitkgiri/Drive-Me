from flask import Flask, render_template, request, redirect,session
from auth.auth import auth
from driveMe.driveMe import driveMe

app = Flask(__name__)
app.register_blueprint(auth, url_prefix="")
app.register_blueprint(driveMe, url_prefix="")
app.secret_key ="hello"

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/testimony")
def testimonies():
    return render_template("testimony.html")

if __name__ == "__main__":
    app.run(debug=True)
