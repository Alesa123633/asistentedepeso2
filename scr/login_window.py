from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton, 
                            QVBoxLayout, QMessageBox, QTabWidget, QWidget, QFormLayout, QSizePolicy)
from PyQt5.QtCore import Qt

class LoginWindow(QDialog):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle("Control de Peso - Inicio de Sesión")
        self.setFixedSize(550, 450)
        self.user_id = None
        self.setup_ui()
        self.setup_styles()

    def setup_ui(self):
        """Configura todos los componentes de la interfaz"""
        self.tabs = QTabWidget()
        
        # Pestaña de Login
        self.login_tab = QWidget()
        self.setup_login_tab()

        # Pestaña de Registro
        self.register_tab = QWidget()
        self.setup_register_tab()

        self.tabs.addTab(self.login_tab, "Iniciar Sesión")
        self.tabs.addTab(self.register_tab, "Registrarse")
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    def setup_styles(self):
        """Estilo unificado con login/registro"""
        self.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
                font-family: Segoe UI;
            }
            QLabel {
                color: #333333;
                font-size: 16px;
                padding: 5px 0;
            }
            QLineEdit {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                color: #000000;
                background-color: #FFFFFF;
                min-width: 250px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 12px 25px;
                border-radius: 8px;
                font-size: 16px;
                border: none;
                min-width: 180px;
            }
            QPushButton:hover {
                background-color: #3E8E41;
            }
            QTabWidget::pane {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 10px;
                background-color: #FFFFFF;
            }
            QTabBar::tab {
                background: #E0E0E0;
                border: 1px solid #CCCCCC;
                padding: 8px 15px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background: #4CAF50;
                color: white;
            }
        """)

    def setup_login_tab(self):
        """Configura la pestaña de login"""
        lbl_title = QLabel("Iniciar Sesión")
        lbl_title.setStyleSheet("font-size: 20px; font-weight: bold;")
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
        """Configura la pestaña de registro"""
        lbl_title = QLabel("Crear Cuenta")
        lbl_title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1565C0;")
        lbl_title.setAlignment(Qt.AlignCenter)
        
        # Campos
        lbl_user = QLabel("Usuario:")
        lbl_user.setMinimumWidth(150)
        self.txt_register_user = QLineEdit()
        self.txt_register_user.setPlaceholderText("Crea un nombre de usuario")
        self.txt_register_user.setMaximumWidth(280)
        
        lbl_pass = QLabel("Contraseña:")
        lbl_pass.setMinimumWidth(150)
        self.txt_register_pass = QLineEdit()
        self.txt_register_pass.setEchoMode(QLineEdit.Password)
        self.txt_register_pass.setPlaceholderText("Cree una contraseña")
        self.txt_register_pass.setMaximumWidth(280)
        
        lbl_confirm = QLabel("Confirmar Contraseña:")
        lbl_confirm.setMinimumWidth(165)
        self.txt_register_confirm = QLineEdit()
        self.txt_register_confirm.setEchoMode(QLineEdit.Password)
        self.txt_register_confirm.setPlaceholderText("Repita la contraseña")
        self.txt_register_confirm.setMaximumWidth(280)
        
        btn_register = QPushButton("Registrarse")
        btn_register.clicked.connect(self.handle_register)
        btn_register.setMaximumWidth(200)
        
        # Layout de formulario
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignHCenter | Qt.AlignTop)
        form_layout.setHorizontalSpacing(18)
        form_layout.setVerticalSpacing(18)
        form_layout.addRow(lbl_user, self.txt_register_user)
        form_layout.addRow(lbl_pass, self.txt_register_pass)
        form_layout.addRow(lbl_confirm, self.txt_register_confirm)
        
        # Contenedor para centrar el formulario
        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(25)
        main_layout.addSpacing(10)
        main_layout.addWidget(lbl_title)
        main_layout.addSpacing(10)
        main_layout.addWidget(form_widget, alignment=Qt.AlignHCenter)
        main_layout.addSpacing(10)
        main_layout.addWidget(btn_register, alignment=Qt.AlignHCenter)
        main_layout.addStretch()
        
        self.register_tab.setLayout(main_layout)

    def handle_login(self):
        """Maneja el intento de login"""
        username = self.txt_login_user.text().strip()
        password = self.txt_login_pass.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Todos los campos son requeridos")
            return
        
        success, user_id = self.db_manager.verify_user(username, password)
        
        if success:
            self.user_id = user_id
            self.username = username
            self.accept()
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
            
        if self.db_manager.register_user(username, password):
            QMessageBox.information(self, "Éxito", "Registro exitoso. Ahora inicia sesión.")
            self.tabs.setCurrentIndex(0)
            self.txt_register_user.clear()
            self.txt_register_pass.clear()
            self.txt_register_confirm.clear()
        else:
            QMessageBox.critical(self, "Error", "El usuario ya existe o hubo un error")