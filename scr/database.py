import sqlite3
from sqlite3 import Error
import hashlib
import os

class DatabaseManager:
    """Clase para manejar todas las operaciones de base de datos"""
    def __init__(self):
        self.initialize_database()
    
    def create_connection(self):
        """Crea conexión a la base de datos usando ruta absoluta"""
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(base_dir, '..', 'database', 'diet_tracker.db')
            conn = sqlite3.connect(db_path)
            return conn
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    def initialize_database(self):
        """Inicializa la base de datos con tablas necesarias"""
        conn = self.create_connection()
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
                print(f"Error al inicializar la base de datos: {e}")
            finally:
                if conn:
                    conn.close()

    # Resto de los métodos permanecen igual...

    def hash_password(self, password):
        """Genera hash SHA-256 de la contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        """Registra un nuevo usuario"""
        conn = self.create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                
                # Insertar usuario
                cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
                user_id = cursor.lastrowid
                
                # Insertar credenciales
                cursor.execute(
                    "INSERT INTO credentials (user_id, password_hash) VALUES (?, ?)",
                    (user_id, self.hash_password(password))
                )
                
                conn.commit()
                return True
            except Error as e:
                print(e)
                return False
            finally:
                conn.close()
        return False

    def verify_user(self, username, password):
        """Verifica las credenciales del usuario"""
        conn = self.create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT users.id, credentials.password_hash 
                    FROM users JOIN credentials ON users.id = credentials.user_id
                    WHERE users.username = ?
                ''', (username,))
                
                result = cursor.fetchone()
                if result and result[1] == self.hash_password(password):
                    return True, result[0]
                return False, None
            except Error as e:
                print(e)
                return False, None
            finally:
                conn.close()
        return False, None

    def add_meal(self, user_id, food_name, meal_type, time):
        """Añade una nueva comida a la base de datos"""
        conn = self.create_connection()
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

    def get_user_meals(self, user_id):
        """Obtiene las comidas de un usuario"""
        conn = self.create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                # Datos para el gráfico circular
                cursor.execute('''
                    SELECT meal_type, COUNT(*) 
                    FROM meals 
                    WHERE user_id = ? 
                    GROUP BY meal_type
                ''', (user_id,))
                meal_data = cursor.fetchall()
                # Datos para la tabla (últimos 15 registros, incluyendo el ID)
                cursor.execute('''
                    SELECT id, date(date) as fecha, meal_type, food_name, time 
                    FROM meals 
                    WHERE user_id = ? 
                    ORDER BY date DESC 
                    LIMIT 15
                ''', (user_id,))
                meals = cursor.fetchall()
                return meal_data, meals
            except Error as e:
                print(e)
                return None, None
            finally:
                conn.close()
        return None, None

    def delete_meal(self, meal_id):
        """Elimina una comida de la base de datos por su ID"""
        conn = self.create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM meals WHERE id = ?', (meal_id,))
                conn.commit()
                return cursor.rowcount > 0
            except Error as e:
                print(e)
                return False
            finally:
                conn.close()
        return False