# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton, 
                            QVBoxLayout, QMessageBox, QTabWidget, QWidget)
from PyQt5.QtCore import Qt
from database import register_user, verify_user

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Peso - Inicio de Sesión")
        self.setFixedSize(550, 450)
        self.user_id = None  # Para almacenar el ID del usuario logeado
        self.setup_ui()
        self.setup_styles()

    def setup_ui(self):
        """Configura todos los componentes de la interfaz"""
        # Crear pestañas (Login y Registro)
        self.tabs = QTabWidget()
        
        # Pestaña de Login
        # En el método setup_ui (o donde tengas el error)
        self.tabs = QTabWidget()

        # Pestaña de Login
        self.login_tab = QWidget()  # <-- Usa self, no elf
        self.setup_login_tab()

        # Pestaña de Registro
        self.register_tab = QWidget()  # <-- Usa self, no elf
        self.setup_register_tab()

        self.tabs.addTab(self.login_tab, "Iniciar Sesión")
        self.tabs.addTab(self.register_tab, "Registrarse")
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    # Reemplaza todo el setup_styles() en food_form.py con:
    def setup_styles(self):
        """Estilo unificado con login/registro"""
        self.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5; /* Mismo fondo gris claro */
                font-family: Segoe UI;
            }
            QLabel {
                color: #333333;
                font-size: 16px;  /* Tamaño aumentado */
                padding: 5px 0;
            }
            QLineEdit {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 10px;   /* Más espacio interno */
                font-size: 16px; /* Tamaño aumentado */
                color: #000000;  /* Texto negro sólido */
                background-color: #FFFFFF;
                min-width: 250px;
            }
            QPushButton {
                background-color: #4CAF50; /* Verde como en login */
                color: white;
                padding: 12px 25px;
                border-radius: 8px;
                font-size: 16px;
                border: none;
                min-width: 180px;
            }
            QPushButton:hover {
                background-color: #3E8E41; /* Verde oscuro al pasar mouse */
            }
            QTimeEdit {
                padding: 8px;
                font-size: 16px;
                min-width: 120px;
                background-color: #FFFFFF;
            }
        """)
    
    # Estilo especial para el título
        title = self.findChild(QLabel)
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2E7D32; /* Verde oscuro */
            padding-bottom: 20px;
        """)

    def setup_login_tab(self):
        """Configura la pestaña de login con letras grandes"""
    # ESTILO IDÉNTICO AL REGISTRO
        self.login_tab.setStyleSheet("""
            QLabel {
                font-size: 18px;
                padding: 8px 0;
            }
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                min-height: 30px;
            }
        """)
    
    # Mantén todo tu código existente igual debajo de esto
        lbl_title = QLabel("Iniciar Sesión")
        lbl_title.setStyleSheet("font-size: 20px; font-weight: bold;")
    
    # ... resto de tu código actual
        lbl_title.setAlignment(Qt.AlignCenter)
        
        lbl_user = QLabel("Usuario:")
        self.txt_login_user = QLineEdit()
        self.txt_login_user.setPlaceholderText("Ingrese su usuario")
        
        lbl_pass = QLabel("Contraseña:")
        self.txt_login_pass = QLineEdit()
        self.txt_login_pass.setEchoMode(QLineEdit.Password)
        self.txt_login_pass.setPlaceholderText("Ingrese su contraseña")
        
        btn_login = QPushButton("Ingresar")
        btn_login.clicked.connect(self.handle_login)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(lbl_title)
        layout.addSpacing(15)
        layout.addWidget(lbl_user)
        layout.addWidget(self.txt_login_user)
        layout.addWidget(lbl_pass)
        layout.addWidget(self.txt_login_pass)
        layout.addSpacing(20)
        layout.addWidget(btn_login, alignment=Qt.AlignCenter)
        
        self.login_tab.setLayout(layout)

    def setup_register_tab(self):
        """Configura la pestaña de registro con letras más grandes"""
        # Estilo específico para registro
        self.register_tab.setStyleSheet("""
            QLabel {
                font-size: 18px;  /* Tamaño aumentado */
                padding: 8px 0;
                color: #333333;
            }
            QLineEdit {
                font-size: 16px;  /* Tamaño aumentado */
                padding: 10px;
                min-height: 35px;
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
            }
        """)
    
    # El resto de tu código de registro permanece igual
        lbl_title = QLabel("Crear Cuenta")
        lbl_title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1565C0;")
    
    # ... (mantén el resto de tu código existente)
    
        lbl_user = QLabel("Usuario:")
        self.txt_register_user = QLineEdit()
        self.txt_register_user.setPlaceholderText("Crea un nombre de usuario")
    
    # ... (todo lo demás sigue exactamente igual)
        lbl_pass = QLabel("Contraseña:")
        self.txt_register_pass = QLineEdit()
        self.txt_register_pass.setEchoMode(QLineEdit.Password)
        self.txt_register_pass.setPlaceholderText("Cree una contraseña")
        
        lbl_confirm = QLabel("Confirmar Contraseña:")
        self.txt_register_confirm = QLineEdit()
        self.txt_register_confirm.setEchoMode(QLineEdit.Password)
        self.txt_register_confirm.setPlaceholderText("Repita la contraseña")
        
        btn_register = QPushButton("Registrarse")
        btn_register.clicked.connect(self.handle_register)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(lbl_title)
        layout.addSpacing(15)
        layout.addWidget(lbl_user)
        layout.addWidget(self.txt_register_user)
        layout.addWidget(lbl_pass)
        layout.addWidget(self.txt_register_pass)
        layout.addWidget(lbl_confirm)
        layout.addWidget(self.txt_register_confirm)
        layout.addSpacing(20)
        layout.addWidget(btn_register, alignment=Qt.AlignCenter)
        
        self.register_tab.setLayout(layout)

    def handle_login(self):
        """Maneja el intento de login"""
        username = self.txt_login_user.text().strip()
        password = self.txt_login_pass.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Todos los campos son requeridos")
            return
        
        success, user_id = verify_user(username, password)
        
        if success:
            self.user_id = user_id
            self.accept()  # Cierra el diálogo con estado "Accepted"
        else:
            QMessageBox.critical(self, "Error", "Usuario o contraseña incorrectos")
            self.txt_login_pass.clear()

    def handle_register(self):
        """Maneja el registro de nuevo usuario"""
        username = self.txt_register_user.text().strip()
        password = self.txt_register_pass.text().strip()
        confirm = self.txt_register_confirm.text().strip()
        
        if not username or not password or not confirm:
            QMessageBox.warning(self, "Error", "Todos los campos son requeridos")
            return
            
        if password != confirm:
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden")
            self.txt_register_pass.clear()
            self.txt_register_confirm.clear()
            return
            
        if len(password) < 6:
            QMessageBox.warning(self, "Error", "La contraseña debe tener al menos 6 caracteres")
            return
            
        if register_user(username, password):
            QMessageBox.information(self, "Éxito", "Registro exitoso. Ahora inicia sesión.")
            self.tabs.setCurrentIndex(0)  # Cambia a pestaña de login
            self.txt_register_user.clear()
            self.txt_register_pass.clear()
            self.txt_register_confirm.clear()
        else:
            QMessageBox.critical(self, "Error", "El usuario ya existe o hubo un error")

# Código para prueba directa
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    window = LoginWindow()
    window.show()
    app.exec_()
