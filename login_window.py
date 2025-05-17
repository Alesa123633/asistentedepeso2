import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, 
    QTabWidget, QWidget, QLabel, 
    QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Peso")
        self.setFixedSize(500, 400)  # Tamaño fijo suficiente
        
        # Configuración ESPECIAL para macOS
        self.setStyleSheet("""
            QTabBar::tab {
                padding: 10px;
                background: #f0f0f0;
                border: 1px solid #aaa;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #fff;
                border-color: #777;
            }
            QTabWidget::pane {
                border: 1px solid #777;
                margin-top: -1px;
            }
        """)
        
        self.init_ui()
    
    def init_ui(self):
        # Widget de pestañas (PRINCIPAL)
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)  # Mejor visualización en macOS
        
        # Pestaña 1: Login
        tab_login = QWidget()
        login_layout = QVBoxLayout(tab_login)
        
        lbl_login = QLabel("INICIAR SESIÓN")
        lbl_login.setAlignment(Qt.AlignCenter)
        lbl_login.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        self.txt_user = QLineEdit(placeholderText="Usuario")
        self.txt_pass = QLineEdit(placeholderText="Contraseña", echoMode=QLineEdit.Password)
        btn_login = QPushButton("Ingresar")
        btn_login.setStyleSheet("background-color: #4CAF50; color: white;")
        
        login_layout.addWidget(lbl_login)
        login_layout.addWidget(QLabel("Usuario:"))
        login_layout.addWidget(self.txt_user)
        login_layout.addWidget(QLabel("Contraseña:"))
        login_layout.addWidget(self.txt_pass)
        login_layout.addWidget(btn_login)
        login_layout.addStretch()
        
        # Pestaña 2: Registro (OBLIGATORIA)
        tab_register = QWidget()
        register_layout = QVBoxLayout(tab_register)
        
        lbl_register = QLabel("REGISTRARSE")
        lbl_register.setAlignment(Qt.AlignCenter)
        lbl_register.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        self.reg_user = QLineEdit(placeholderText="Nuevo usuario")
        self.reg_pass = QLineEdit(placeholderText="Contraseña", echoMode=QLineEdit.Password)
        self.reg_confirm = QLineEdit(placeholderText="Confirmar contraseña", echoMode=QLineEdit.Password)
        btn_register = QPushButton("Crear cuenta")
        btn_register.setStyleSheet("background-color: #2196F3; color: white;")
        
        register_layout.addWidget(lbl_register)
        register_layout.addWidget(QLabel("Usuario:"))
        register_layout.addWidget(self.reg_user)
        register_layout.addWidget(QLabel("Contraseña:"))
        register_layout.addWidget(self.reg_pass)
        register_layout.addWidget(QLabel("Confirmar:"))
        register_layout.addWidget(self.reg_confirm)
        register_layout.addWidget(btn_register)
        register_layout.addStretch()
        
        # Añadir pestañas (VISIBLES)
        self.tabs.addTab(tab_login, "Iniciar Sesión")
        self.tabs.addTab(tab_register, "Registrarse")
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.tabs)
        
        # Conexiones
        btn_login.clicked.connect(self.login)
        btn_register.clicked.connect(self.register)
        
        # TRUCO FINAL: Forzar visibilidad
        self.tabs.setCurrentIndex(1)  # Mostrar primero registro
        self.tabs.setCurrentIndex(0)  # Volver a login
    
    def login(self):
        QMessageBox.information(self, "Login", "Función de login")
    
    def register(self):
        if self.reg_pass.text() != self.reg_confirm.text():
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden")
            return
        QMessageBox.information(self, "Éxito", "Usuario registrado")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # ¡ESENCIAL para macOS!
    
    window = LoginWindow()
    window.show()
    
    sys.exit(app.exec_())