import sqlite3

DB_NAME = "database.sqlite"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn