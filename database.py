import sqlite3
import hashlib

# from flask import Flask

DB_FILE="database.db"

###############
#             #
# Basic Setup #
#             #
###############

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor() #creates a cursor, which is an object that helps fetch records from the database

# Create tables if they don't exist
c.execute("""
    CREATE TABLE IF NOT EXISTS users (
      username TEXT,
      password TEXT,
      highScore INTEGER
    )""")

#####################
#                   #
# Utility Functions #
#                   #
#####################
#liesel plz make a function that rewrites database file
def get_hash_pass(password):
    # password = "really-secure-password123"
    password = password.encode() # converts your string to bytes
    password_hash = hashlib.sha512(password) # use the sha-512 algorithm to generate a hash digest
    return password_hash.hexdigest() # prints the hash digest as a sequence of base-16 digits
    # return password_hash.hexdigest()

def check_hash(username, password):
    given_pass = get_hash_pass(password)
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM users WHERE password = (?)", (given_pass,))
    row = c.fetchone()
    db.close()

    return row is not None

def register_user(username, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    #single quotes doesn't let you add in newlines
    c.execute("SELECT * FROM users WHERE LOWER(username) = LOWER(?)", (username,))
    row = c.fetchone()

    if row is not None:
        db.close()
        return False

    hashed_pass = get_hash_pass(password)
    c.execute("""INSERT INTO users (username, password) VALUES(?, ?)""", (username, hashed_pass))
    db.commit()
    db.close()
    return True

def check_login(username, password):
    """
    Tries to add the given username and password into the database.
    Returns False if the user already exists, True if it successfully added the user.
    """
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    hashed_pass = get_hash_pass(password)
    print("hashed_pass:", hashed_pass)
    c.execute("SELECT * FROM users WHERE LOWER(username) = LOWER(?) AND password = ?", (username,hashed_pass))
    row = c.fetchone()
    print("row:", row)
    db.close()

    return row is not None

def display_score(username):
    # print("good0")
    # Returns password from inputed username
    db = sqlite3.connect(DB_FILE)
    cur = db.cursor()
    # print("good1")
    cur.execute("SELECT highScore FROM users WHERE LOWER(username) = LOWER(?)", (username,))
    # print("good2")
    score = cur.fetchone()[0]
    if score is None:
        return 0
    else:
        return score

def update_score(username, score):
    db = sqlite3.connect(DB_FILE)
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE LOWER(username) = LOWER(?)", (username,))
    row = cur.fetchone()
    # print(row)
    # print("hi")
    if row is None:
        db.close()
        return False

    cur.execute("""UPDATE users SET highScore = (?) WHERE LOWER(username) = LOWER(?)""", (score, username))
    db.commit()
    db.close()
    return True

def delete_all():
    db = sqlite3.connect(DB_FILE)
    cur = db.cursor()
    cur.execute("""DELETE FROM users WHERE TRUE""")
    db.commit()
    db.close()

def display():
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    db = sqlite3.connect(DB_FILE)
    cur = db.cursor()
    cur.execute("SELECT * FROM users")

    rows = cur.fetchall()

    for row in rows:
        print(row)
