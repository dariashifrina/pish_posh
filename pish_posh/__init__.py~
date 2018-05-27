from flask import Flask, url_for,render_template, session
from os import path


app = Flask(__name__)

DIR = path.dirname(__file__)


#console output will appear in /var/log/apache2/error.log

@app.route('/')
def root():
    if "username" in session:
        return redirect(url_for("homepage"))

    return render_template("login.html")

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if "username" not in session:
        return render_template("signup.html")
    else:
        flash("you are logged in")
        return redirect(url_for("homepage"))


@app.route('/homepage', methods=["GET","POST"])
def homepage():
    if "username" in session:
        username = session["username"]

if __name__ == '__main__':
    app.debug = True #DANGER DANGER! Set to FALSE before deployment!
    app.run()
