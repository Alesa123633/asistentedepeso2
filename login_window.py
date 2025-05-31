# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, 
                            QPushButton, QVBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt
import sys  # Nuevo import añadido

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        # Configuración básica de la ventana
        self.setWindowTitle("Sistema de Dietas - Login V2")
        self.setFixedSize(400, 300)
        
        # ESTILOS VISIBLES (aseguran que los componentes se vean)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                font-family: Arial;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
                padding: 5px;
            }
            QLineEdit {
                border: 2px solid #3498db;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                min-width: 200px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
        """)

        # COMPONENTES VISIBLES (aseguran que haya contenido)
        self.lbl_title = QLabel("INICIO DE SESIÓN (VERSIÓN VISIBLE)")
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.lbl_title.setStyleSheet("font-size: 20px; color: #e74c3c; font-weight: bold;")
        
        self.txt_username = QLineEdit()
        self.txt_username.setPlaceholderText("Ejemplo: usuario123")
        
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.setPlaceholderText("Ingresa tu contraseña")
        
        self.btn_login = QPushButton("Acceder al Sistema")
        
        # LAYOUT CON MÁRGENES VISIBLES
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        layout.addWidget(self.lbl_title)
        layout.addWidget(QLabel("Usuario:"))
        layout.addWidget(self.txt_username)
        layout.addWidget(QLabel("Contraseña:"))
        layout.addWidget(self.txt_password)
        layout.addWidget(self.btn_login)
        
        # ASIGNAR LAYOUT (esto hace que los componentes se muestren)
        self.setLayout(layout)

        # Conexión del botón para verificar funcionalidad
        self.btn_login.clicked.connect(lambda: QMessageBox.information(
            self, "Prueba", "¡El botón funciona correctamente!"))

# Código de prueba directa
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
