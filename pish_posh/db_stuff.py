import sqlite3
import hashlib
import json

DB = "pish.db"

'''
def user_tables():
    db = sqlite3.connect(DB)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS students (username TEXT, password TEXT, osis INTEGER, student_id INTEGER, user_id INTEGER PRIMARY KEY)")
    c.execute("CREATE TABLE IF NOT EXISTS teachers (username TEXT, password TEXT, user_id INTEGER PRIMARY KEY)")
    db.commit()
    db.close()
'''
#################students DB FXNS#################################
def add_student(name, lastname, username, password, osis, sid):
#    user_tables()
    db = sqlite3.connect(DB)
    c = db.cursor()
    query = 'SELECT * FROM students WHERE username = ?'
    check = c.execute(query, (username,))
    id = get_id('students','SID')
    if not check.fetchone():
        new_pass = hashlib.sha256(password).hexdigest()
        c.execute('INSERT INTO students VALUES (?,?,?,?,?,?)', (name,lastname, username, new_pass, osis, sid))
        c.execute('INSERT INTO student_info VALUES (?, ?)', (sid, '[]'))
        db.commit()
        db.close()
        return True
    db.commit()
    db.close()
    return False

def get_id(table, param='CID'): #autmatically detects a new id
    db = sqlite3.connect(DB)
    c = db.cursor()
    query = 'SELECT '+ param + ' FROM ' + table #SQL was giving me a weird error so I hardcoded
    ids = c.execute(query)
    id = 0;
    for iter in ids:
        id+=1
    print id

def add_class(name, tid, slist, desc):
    db = sqlite3.connect(DB)
    c = db.cursor()
    cid=get_id('classes')
    c.execute('INSERT INTO classes VALUES (?,?,?,?,?)', (cid, name, tid, slist, desc))
    db.commit()
    db.close()
    return True

def add_work(cid, wdescr, type, date):
    db = sqlite3.connect(DB)
    c = db.cursor()
    c.execute('INSERT INTO class_work VALUES (?,?,?,?)', (cid, type, date, wdescr))
    db.commit()
    db.close()
    return True

def change_pass(username, password0):
    db = sqlite3.connect(DB)
    c = db.cursor()
    comm = 'UPDATE students SET password = ? WHERE username = ?'
    c.execute(comm, (hashlib.sha256(password0).hexdigest(), username))
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
    id = ret[5]
    db.close()
    return id

def get_name_from_student(username):
    db = sqlite3.connect(DB)
    c = db.cursor()
    query = 'SELECT * FROM students WHERE username = ?'
    check = c.execute(query, (username,))
    ret = None
    for q in check:
        ret = q
    fname = ret[0]
    lname = ret[1]
    name = []
    name.append(fname)
    name.append(lname)
    db.close()
    return name

def get_pass_from_student(username):
    db = sqlite3.connect(DB)
    c = db.cursor()
    query = 'SELECT * FROM students WHERE username = ?'
    check = c.execute(query, (username,))
    ret = None
    for q in check:
        ret = q
    password = ret[3]
    db.close()
    return password

def get_osis_from_student(username):
    db = sqlite3.connect(DB)
    c = db.cursor()
    query = 'SELECT * FROM students WHERE username = ?'
    check = c.execute(query, (username,))
    ret = None
    for q in check:
        ret = q
    osis = ret[4]
    db.close()
    return osis

def get_classes_from_id(sid):
    db = sqlite3.connect(DB)
    c = db.cursor()
    query = 'SELECT * FROM student_info WHERE SID = ?'
    check = c.execute(query, (sid,))
    print check
    ret = None
    try:
        for q in check:
            ret = q
        clist = ret[1]
    except:
        clist = []
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
    clist = [ret[0], ret[1], ret[4]]
    db.close()
    return clist

def get_classes_from_list(lst):
    ret = []
    for num in lst:
        ret.append(get_class_from_cid(num))
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
    comm = 'UPDATE student_info SET CList = ? WHERE SID = ?'
    c.execute(comm, (ncl, id))
    db.commit()
    db.close()

def get_classes_from_student(username):
    id = get_id_from_student(username)
    print id
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

#print get_classes_from_student("a")
#add_student('Karina', 'kionkina', 'Boop1', 209853738, 4193)

#######teachers DB FXNS##########################################
def add_teacher(firstname, lastname, username, password):
#    user_tables()
    db = sqlite3.connect(DB)
    c = db.cursor()
    query = 'SELECT * FROM teachers WHERE username = ?'
    check = c.execute(query, (username,))
    if not check.fetchone():
        new_pass = hashlib.sha256(password).hexdigest()
        c.execute('INSERT INTO teachers(username, fname, lname,password, CList) VALUES (?,?,?,?,?)', (username,firstname, lastname, new_pass, ""))
        #c.execute('INSERT INTO teachers VALUES (?,?,?,?,?,?)', (firstname,lastname, username, password, ""))
#        c.execute('INSERT INTO student_info VALUES (?, ?)', (sid, '[]'))
        db.commit()
        db.close()
        return True
    db.commit()
    db.close()
    return False

def teacherauth(username, password):
    db = sqlite3.connect(DB)
    c = db.cursor()
    passs = hashlib.sha256(password).hexdigest()
    query = 'SELECT password FROM teachers WHERE username = ? AND password = ?'
    check = c.execute(query, (username, passs))
    ret = check.fetchone()
    print ret
    db.close()
    return ret

#######admin DB FXNS##########################################

def adminauth(username, password):
    db = sqlite3.connect(DB)
    c = db.cursor()
    passs = hashlib.sha256(password).hexdigest()
    query = 'SELECT password FROM admins WHERE username = ? AND password = ?'
    check = c.execute(query, (username, passs))
    ret = check.fetchone()
    print ret
    db.close()
    return ret


def get_tid_from_teacher(username):
    db = sqlite3.connect(DB)
    c = db.cursor()
    query = "SELECT TID FROM teachers where username = '" + username + "'"
    tid = c.execute(query).fetchall()
    print tid[0][0]

def get_classes_from_teacher(tid):
    db = sqlite3.connect(DB)
    c = db.cursor()
    query = "SELECT TID FROM teachers where TID = '" + tid + "'"
    classes = c.execute(query).fetchall()
