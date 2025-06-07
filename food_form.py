from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
                           QVBoxLayout, QTimeEdit, QMessageBox, QGridLayout, QHBoxLayout)
from PyQt5.QtCore import QTime, Qt

class FoodForm(QWidget):
    def __init__(self, user_id, username):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle(f"Dieta de {username}")
        self.setFixedSize(650, 550)  # Tamaño ligeramente mayor
        self.setup_ui()
        self.setup_styles()

    def setup_ui(self):
        """Configuración mejorada de la interfaz"""
        # Título principal
        lbl_title = QLabel("Registro de Alimentos")
        lbl_title.setAlignment(Qt.AlignCenter)
        
        # Campos para alimentos (5 campos)
        self.food_inputs = []
        grid = QGridLayout()
        for i in range(5):
            lbl = QLabel(f"Alimento {i+1}:")
            input_field = QLineEdit()
            input_field.setPlaceholderText(f"¿Qué comiste en el alimento {i+1}?")
            self.food_inputs.append(input_field)
            grid.addWidget(lbl, i, 0)
            grid.addWidget(input_field, i, 1)
        
        # Selector de hora mejorado
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("hh:mm AP")
        self.time_edit.setTime(QTime.currentTime())
        
        # Botón para guardar
        btn_save = QPushButton("💾 Guardar Comida")  # Con icono
        
        # Organización del layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(lbl_title)
        main_layout.addSpacing(20)
        main_layout.addLayout(grid)
        
        # Sección de hora centrada
        time_layout = QHBoxLayout()
        time_layout.addStretch()
        time_layout.addWidget(QLabel("Hora de la comida:"))
        time_layout.addWidget(self.time_edit)
        time_layout.addStretch()
        
        main_layout.addLayout(time_layout)
        main_layout.addSpacing(30)
        main_layout.addWidget(btn_save, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        btn_save.clicked.connect(self.save_meal)

    def setup_styles(self):
        """Estilo unificado y mejorado"""
        self.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
                font-family: Arial;
            }
            QLabel {
                color: #333333;
                font-size: 16px;
                padding: 5px 0;
            }
            QLineEdit {
                border: 2px solid #CCCCCC;
                border-radius: 6px;
                padding: 10px;
                font-size: 16px;
                color: #000000;
                background-color: #FFFFFF;
                min-width: 300px;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 12px 25px;
                border-radius: 8px;
                font-size: 16px;
                border: none;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #3E8E41;
            }
            QTimeEdit {
                padding: 8px;
                font-size: 16px;
                min-width: 120px;
                background-color: #FFFFFF;
            }
        """)
        
        # Estilo especial para el título
        self.findChild(QLabel).setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #2E7D32;
            padding-bottom: 15px;
        """)


    def save_meal(self):
        """Guarda las comidas en la base de datos"""
        from database import add_meal
        
        # Obtener alimentos no vacíos
        foods = [f.text().strip() for f in self.food_inputs if f.text().strip()]
        
        if not foods:
            QMessageBox.warning(self, "Error", "Debe ingresar al menos un alimento")
            return
            
        # Obtener y formatear hora
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
        
        # Mostrar feedback al usuario
        if success_count > 0:
            QMessageBox.information(
                self, 
                "Éxito", 
                f"Se registraron {success_count} alimentos como {meal_type.lower()}\nHora: {time}"
            )
            
            # Limpiar campos (excepto la hora)
            for field in self.food_inputs:
                field.clear()
        else:
            QMessageBox.critical(
                self, 
                "Error", 
                "No se pudieron guardar los alimentos. Intente nuevamente"
            )
