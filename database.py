import sqlite3
from sqlite3 import Error
import hashlib

def create_connection():
    """Crea conexión a la base de datos"""
    conn = None
    try:
        conn = sqlite3.connect('diet_tracker.db')
        return conn
    except Error as e:
        print(e)
    return conn

def initialize_database():
    """Inicializa las tablas"""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS credentials (
                    user_id INTEGER PRIMARY KEY,
                    password_hash TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS meals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    food TEXT NOT NULL,
                    meal_type TEXT NOT NULL,
                    time TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            conn.commit()
        except Error as e:
            print(e)
        finally:
            conn.close()

def hash_password(password):
    """Genera hash de contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    """Registra nuevo usuario"""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
            user_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO credentials (user_id, password_hash) VALUES (?, ?)",
                (user_id, hash_password(password))
            )
            conn.commit()
            return True
        except Error as e:
            print(e)
            return False
        finally:
            conn.close()

def verify_credentials(username, password):
    """Verifica credenciales"""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT users.id, credentials.password_hash 
                FROM users JOIN credentials ON users.id = credentials.user_id
                WHERE users.username = ?
            ''', (username,))
            result = cursor.fetchone()
            if result and result[1] == hash_password(password):
                return True, result[0], "Login exitoso"
            return False, None, "Credenciales inválidas"
        except Error as e:
            print(e)
            return False, None, str(e)
        finally:
            conn.close()
    return False, None, "Error de conexión"