import sqlite3
import hashlib
import json

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

def get_id_from_student(username):
    db = sqlite3.connect(DB)
    c = db.cursor()
    query = 'SELECT * FROM students WHERE username = ?'
    check = c.execute(query, (username,))
    ret = None
    for q in check:
        ret = q
    id = ret[4]
    db.close()
    return id

def get_classes_from_id(id):
    db = sqlite3.connect(DB)
    c = db.cursor()
    query = 'SELECT * FROM student_info WHERE ID = ?'
    check = c.execute(query, (id,))
    ret = None
    for q in check:
        ret = q
    clist = ret[2]
    db.close()
    return clist

def get_class_from_cid(cid):
    db = sqlite3.connect(DB)
    c = db.cursor()
    query = 'SELECT * FROM classes WHERE CID = ?'
    check = c.execute(query, (cid,))
    ret = None
    for q in check:
        ret = q
    clist = str(ret[2]) + " - " + ret[4]
    db.close()
    return clist

def get_classes_from_list(lst):
    ret = ""
    for num in lst:
        ret += get_class_from_cid(num) + "<br>"
    return ret

def append_class(username, cl):
    id = get_id_from_student(username)
    orig = get_classes_from_id(id)
    olst = json.loads(orig)
    olst.append(cl)
    nlist = json.dumps(olst)
    update_classes(id, nlist)

def update_classes(id, ncl):
    db = sqlite3.connect(DB)
    c = db.cursor()
    comm = 'UPDATE student_info SET CList = ? WHERE ID = ?'
    c.execute(comm, (ncl, id))
    db.commit()
    db.close()

def get_classes_from_student(username):
    id = get_id_from_student(username)
    clist = get_classes_from_id(id)
    lst = json.loads(clist)
    class_list = get_classes_from_list(lst)
    return class_list


def auth(username, password):
    db = sqlite3.connect(DB)
    c = db.cursor()
    passs = hashlib.sha256(password).hexdigest()
    query = 'SELECT password FROM students WHERE username = ? AND password = ?'
    check = c.execute(query, (username, passs))
    ret = check.fetchone()
    db.close()
    return ret
