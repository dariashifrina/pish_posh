import sqlite3

DB = "pish.db"

def user_tables():
    db = sqlite3.connect(DB)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS students (username TEXT, password TEXT, osis INTEGER, student_id INTEGER, user_id INTEGER PRIMARY KEY)")
    c.execute("CREATE TABLE IF NOT EXISTS teachers (username TEXT, password TEXT, user_id INTEGER PRIMARY KEY)")
    db.commit()
    db.close()

def add_student(username, password, osis, student_id):
    db = sqlite3.connect(DB)
    c = db.cursor()
    query = 'SELECT * FROM students WHERE username = ?'
    check = c.execute(query, username)
    if not check.fetchone():
        new_pass = hashlib.sha256(password).hexdigest()
        c.execute('INSERT INTO students VALUES (?,?,?,?,NULL)', (username, new_pass, osis, student_id))
        db.commit()
        db.close()
        return True
    db.commit()
    db.close()
    return False

def auth(username, password):
    db = sqlite3.connect(DB)
    c = db.cursor()
    passs = hashlib.sha256(password).hexdigest()
    query = 'SELECT password FROM users WHERE username = ? AND password = ?'
    check = c.execute(query, (username, passs))
    ret = check.fetchone()
    db.close()
    return ret
