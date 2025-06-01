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
    """Inicializa la base de datos con tablas necesarias"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            # Tabla de usuarios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de credenciales
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS credentials (
                    user_id INTEGER PRIMARY KEY,
                    password_hash TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Tabla de comidas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS meals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    food_name TEXT NOT NULL,
                    meal_type TEXT NOT NULL,
                    time TEXT NOT NULL,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            conn.commit()
        except Error as e:
            print(e)
        finally:
            conn.close()

def hash_password(password):
    """Genera hash SHA-256 de la contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    """Registra un nuevo usuario"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            # Insertar usuario
            cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
            user_id = cursor.lastrowid
            
            # Insertar credenciales
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
    return False

def verify_user(username, password):
    """Verifica las credenciales del usuario"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT users.id, credentials.password_hash 
                FROM users JOIN credentials ON users.id = credentials.user_id
                WHERE users.username = ?
            ''', (username,))
            
            result = cursor.fetchone()
            if result and result[1] == hash_password(password):
                return True, result[0]
            return False, None
        except Error as e:
            print(e)
            return False, None
        finally:
            conn.close()
    return False, None

def add_meal(user_id, food_name, meal_type, time):
    """Añade una nueva comida a la base de datos"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO meals (user_id, food_name, meal_type, time)
                VALUES (?, ?, ?, ?)
            ''', (user_id, food_name, meal_type, time))
            conn.commit()
            return True
        except Error as e:
            print(e)
            return False
        finally:
            conn.close()
    return False

# Inicializar la base de datos al importar
initialize_database()
