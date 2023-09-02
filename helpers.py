import sqlite3

# Decorator for database connection handling
def db_connect(func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('database/inscryption.db')
        cursor = conn.cursor()
        result = func(cursor, *args, **kwargs)
        conn.close()
        return result
    return wrapper