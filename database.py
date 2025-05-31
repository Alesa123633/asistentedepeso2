import sqlite3
from sqlite3 import Error

def create_connection():
    """Crea una conexión a la base de datos SQLite"""
    conn = None
    try:
        conn = sqlite3.connect('diet_tracker.db')
        return conn
    except Error as e:
        print(e)
    return conn

def initialize_database():
    """Inicializa las tablas necesarias"""
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS users
                         (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
            conn.commit()
        except Error as e:
            print(e)
        finally:
            conn.close()

# Usuario de prueba
initialize_database()
conn = create_connection()
c = conn.cursor()
c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('admin', 'admin123'))
conn.commit()
conn.close()
