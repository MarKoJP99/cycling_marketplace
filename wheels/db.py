import sqlite3
from flask import g
import os

# set the path to the database
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(BASE_DIR, "db", "wheels_database.db")

print("BASE_DIR:", BASE_DIR)
print("DATABASE:", DATABASE)




def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def search_wheels(search_query):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM wheels WHERE brand LIKE ? OR model_name LIKE ?", ('%' + search_query + '%', '%' + search_query + '%'))
    results = cursor.fetchall()
    cursor.close()
    return results
