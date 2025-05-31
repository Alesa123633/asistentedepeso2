from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class FoodForm(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle(f"Sistema de Dietas - {username}")
        self.setFixedSize(600, 400)
        
        lbl = QLabel(f"Bienvenido {username}\nEsta es la ventana principal")
        lbl.setStyleSheet("font-size: 24px;")
        
        layout = QVBoxLayout()
        layout.addWidget(lbl)
        self.setLayout(layout)
