import sqlite3
import hashlib

DB = "pish.db"

def user_tables():
    db = sqlite3.connect(DB)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS students (username TEXT, password TEXT, osis INTEGER, student_id INTEGER, user_id INTEGER PRIMARY KEY)")
    c.execute("CREATE TABLE IF NOT EXISTS teachers (username TEXT, password TEXT, user_id INTEGER PRIMARY KEY)")
    db.commit()
    db.close()

def add_student(username, password, osis, student_id):
    user_tables()
    db = sqlite3.connect(DB)
    c = db.cursor()
    query = 'SELECT * FROM students WHERE username = ?'
    check = c.execute(query, (username,))
    if not check.fetchone():
        new_pass = hashlib.sha256(password).hexdigest()
        c.execute('INSERT INTO students VALUES (?,?,?,?,NULL)', (username, new_pass, osis, student_id))
        db.commit()
        db.close()
        return True
    db.commit()
    db.close()
    return False

def get_id(table): #autmatically detects a new id
    db = sqlite3.connect(DB)
    c = db.cursor()
    query = 'SELECT CID FROM classes;' #SQL was giving me a weird error so I hardcoded
    ids = c.execute(query)
    id = 0;
    for iter in ids:
        id+=1
    print id

def add_class(name, tid, slist, desc):
    user_tables()
    db = sqlite3.connect(DB)
    c = db.cursor()
    cid=get_id('classes')
    c.execute('INSERT INTO classes VALUES (?,?,?,?,?)', (cid, name, tid, slist, desc))
    db.commit()
    db.close()
    return True

def auth(username, password):
    db = sqlite3.connect(DB)
    c = db.cursor()
    passs = hashlib.sha256(password).hexdigest()
    query = 'SELECT password FROM students WHERE username = ? AND password = ?'
    check = c.execute(query, (username, passs))
    ret = check.fetchone()
    db.close()
    return ret
