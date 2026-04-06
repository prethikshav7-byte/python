import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Hardikpandya_@_33",  # CHANGE THIS
        database="expense_tracker"
    )