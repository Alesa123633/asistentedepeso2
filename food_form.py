from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
                            QVBoxLayout, QHBoxLayout, QTimeEdit, QMessageBox)
from PyQt5.QtCore import QTime, Qt
from PyQt5.QtGui import QFont

class FoodForm(QWidget):
    def __init__(self, user_id, username):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle(f"Control de Peso - {username}")
        self.setFixedSize(600, 500)
        self.setup_ui()

    def setup_ui(self):
        # Configuración de estilo
        self.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                font-family: Segoe UI;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
                padding: 5px 0;
            }
            QLineEdit {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QTimeEdit {
                padding: 6px;
                font-size: 14px;
            }
        """)

        # Título
        lbl_title = QLabel("Registro de Comidas")
        lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1565C0;")
        lbl_title.setAlignment(Qt.AlignCenter)
        
        # Campos para alimentos
        self.food_inputs = []
        for i in range(1, 6):
            lbl = QLabel(f"Alimento {i}:")
            input_field = QLineEdit()
            input_field.setPlaceholderText(f"¿Qué comiste en el alimento {i}?")
            self.food_inputs.append(input_field)
        
        # Selector de hora
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("hh:mm AP")
        self.time_edit.setTime(QTime.currentTime())
        
        # Botón de guardar
        btn_save = QPushButton("Guardar Comida")
        btn_save.clicked.connect(self.save_meal)
        
        # Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(lbl_title)
        main_layout.addSpacing(20)
        
        for i, (lbl, input_field) in enumerate(zip(
            [QLabel("Alimento 1:"), QLabel("Alimento 2:"), QLabel("Alimento 3:"), 
             QLabel("Alimento 4:"), QLabel("Alimento 5:")], self.food_inputs)):
            main_layout.addWidget(lbl)
            main_layout.addWidget(input_field)
            if i < 4:
                main_layout.addSpacing(10)
        
        main_layout.addSpacing(15)
        main_layout.addWidget(QLabel("Hora de la comida:"))
        main_layout.addWidget(self.time_edit)
        main_layout.addSpacing(20)
        main_layout.addWidget(btn_save, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        
        self.setLayout(main_layout)

    def save_meal(self):
        from database import add_meal
        
        foods = [f.text().strip() for f in self.food_inputs if f.text().strip()]
        
        if not foods:
            QMessageBox.warning(self, "Error", "Debe ingresar al menos un alimento")
            return
            
        time = self.time_edit.time().toString("hh:mm AP")
        hour = self.time_edit.time().hour()
        
        # Determinar tipo de comida según la hora
        if hour < 12:
            meal_type = "Desayuno"
        elif 12 <= hour < 18:
            meal_type = "Comida"
        else:
            meal_type = "Cena"
        
        # Guardar cada alimento
        success_count = 0
        for food in foods:
            if add_meal(self.user_id, food, meal_type, time):
                success_count += 1
        
        if success_count > 0:
            QMessageBox.information(self, "Éxito", 
                f"Se registraron {success_count} alimentos como {meal_type.lower()}")
            
            # Limpiar campos
            for field in self.food_inputs:
                field.clear()
        else:
            QMessageBox.critical(self, "Error", "No se pudieron guardar los alimentos")
