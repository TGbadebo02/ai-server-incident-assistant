import sqlite3


def get_connection():
    connection = sqlite3.connect("incidents.db")
    return connection
