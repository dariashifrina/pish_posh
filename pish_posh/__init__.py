from flask import Flask, redirect, url_for,render_template, session, request, flash
import os
from os import path
import sqlite3
import db_stuff


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
        return render_template("home.html", username = session["username"])
    return redirect(url_for("auth"))


@app.route('/auth', methods=["GET", "POST"])
def auth():
    if "username" in session:
        return redirect(url_for("homepage"))
    if request.method == "GET":
        return redirect("/")
    try:
        username = request.form['username']
        password = request.form['password']
        #osis = request.form['osis']
        #student_id = request.form['student_id']

    except KeyError:
        print 'test'
        flash("Please fill everything in!")
        return render_template("login.html")

    '''
    db authentication
    '''
    if db_stuff.auth(username,password):
        session['username'] = username
        flash("You're logged in!")
        return redirect(url_for("homepage"))
    else:
        flash("oops! Login failed...")
        return redirect(url_for('login'))

def min_thres(pswd):
    '''
    Returns whether a password meets minimum threshold:
    It contains a mixture of upper- and lowercase letters, and at least one number
    '''
    UC_LETTERS = "QWERTYUIOPASDFGHJKLZXCVBNM"
    LC_LETTERS = UC_LETTERS.lower()
    NUMBERS = "1234567890"
    U= [1 if x in UC_LETTERS else 0 for x in pswd]
    L= [1 if x in LC_LETTERS else 0 for x in pswd]
    N = [1 if x in NUMBERS else 0 for x in pswd]
    upper = 1 in U
    lower = 1 in L
    num = 1 in N
    return upper and lower and num


@app.route('/signauth', methods = ["GET", "POST"])
def signauth():
    if "username" in session:
        return redirect(url_for("homepage"))
    if request.method == "GET":
        return redirect("/")
    try:
        username = request.form['username']
        password0 = request.form['password0']
        password1 = request.form['password1']
        osis = request.form['osis']
        student_id = request.form['student_id']
    except KeyError:
        flash("Fill evrything in!")
        return render_template("signup.html")
    if password0 != password1:
        flash("Passwords don't match!")
        return render_template("signup.html")
    if not min_thres(password0):
        flash("Password must contain upper- and lowercase letters and at least one number")
        return render_template("signup.html")
    if db_stuff.add_student(username, password0, osis, student_id):
        flash("successfully created!")
        return redirect(url_for("homepage"))
    else:
        flash("username exists")
        return render_template("signup.html")


if __name__ == '__main__':
    app.secret_key = os.urandom(32)
    app.debug = True #DANGER DANGER! Set to FALSE before deployment!
    app.run()
