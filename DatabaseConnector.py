

import mysql.connector
import os

# Establish a connection to the MySQL database

def connect_db():
    db = mysql.connector.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        port=os.getenv("PORT"),
        database=os.getenv("DB"),
    )
    return db

all_db = []

max_id = 0

#This function prints out the DB
def print_db(db):
    cursor = db.cursor()
    get_query = "SELECT id, username, password FROM golfers"
    cursor.execute(get_query)
    print(cursor.fetchall())

#This function clears the submissions table
def clear_db(db):
    cursor = db.cursor()
    clear_query = "DELETE FROM submissions"
    cursor.execute(clear_query)
    db.commit()
    cursor.close()
    print("Database cleared")

#This function takes in a username and deletes them from the DB
def delete_user_by_name(db, uname, passw):
    cursor = db.cursor()
    delete_user_query = "DELETE FROM golfers WHERE username = %s AND password = %s"
    cursor.execute(delete_user_query, (uname, passw ))
    db.commit()
    print("User deleted")
    cursor.close()
#This function takes in a username and outputs returns a password
def get_id_from_username(db, uname):
    cursor = db.cursor()
    get_id_query = "SELECT id FROM golfers WHERE username = %s"
    cursor.execute(get_id_query, (uname,))
    result = cursor.fetchone()
    cursor.close()
    return result[0]



#This fucntion takes in a username and returns a boolean as to whether or not they are in the database
def is_in_db(db, uname):
    cursor = db.cursor()
    check_query = "SELECT * FROM golfers WHERE username = %s;"
    cursor.execute(check_query, (uname, ))
    results = cursor.fetchall()
    for result in results:
        if result[1] == uname:
            cursor.close()
            return True
        return False
#This function takes in an ID, Score, and a Date to add to the submissions table
def insert_submission(db, id, score, date):
    cursor = db.cursor()
    insert_query = "INSERT INTO submissions (id, score, entrydate) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (id, score, date))
    db.commit()
    cursor.close()
    print("Submission put into DB!")



#This function takes a username and password and adds to golfers table
def insert_golfer(db, uname, passw):
    cursor = db.cursor()
    insert_query = "INSERT INTO golfers (username, password) VALUES (%s, %s)"
    cursor.execute(insert_query, (uname, passw))
    cursor.close()
    db.commit()

    print("Data put into DB!")




def reset_increment(index):

    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM golfers")
    print("Now I'm here")
    count = cursor.fetchone()[0]
    if count == 0:
        reset_query = "ALTER TABLE golfers AUTO_INCREMENT = 0"
        cursor.execute(reset_query)
        print("Increment now at 0")
    else:
        print("I didn't get to the condition")


    cursor.close()
#This function takes in a username and password and then returns whether or not that password is correct for that username
def get_password(db, uname, passw):
    cursor = db.cursor()
    pass_query = ("SELECT password FROM golfers WHERE username = %s")
    cursor.execute(pass_query, (uname, ))
    results = cursor.fetchall()
    if passw == results[0][0]:
        cursor.close()
        return True
    return False
#This function takes in an ID and gets all of their submissions from the submissions table
def get_user_submissions(db, id):
    recents = []
    cursor = db.cursor()
    submissions_query = ("SELECT score, entrydate FROM submissions WHERE id = %s")
    cursor.execute(submissions_query, (id,))
    entries = cursor.fetchall()
    for entry in entries:
        submission = entry[1].date(), entry[0]
        recents.append(submission)
    return recents

db = connect_db()
#insert(db, "john", "password1")
print_db(db)
#clear_db(db)
#delete_user_by_name("andrew", "1")
#reset_increment(0)
#print(is_in_db(db, "john"))