from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
                           QVBoxLayout, QTimeEdit, QMessageBox, QGridLayout, QHBoxLayout)
from PyQt5.QtCore import QTime, Qt

class FoodForm(QWidget):
    def __init__(self, user_id, username, db_manager, main_window):
        super().__init__()
        self.user_id = user_id
        self.db_manager = db_manager
        self.main_window = main_window
        self.setWindowTitle(f"Dieta de {username}")
        self.setFixedSize(650, 550)
        self.setup_ui()
        self.setup_styles()

    def setup_ui(self):
        """Configuración mejorada de la interfaz"""
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
        
        # Botones
        btn_save = QPushButton("💾 Guardar Comida")
        btn_save.clicked.connect(self.save_meal)
        
        btn_back = QPushButton("🔙 Volver al Dashboard")
        btn_back.clicked.connect(self.go_back_to_dashboard)
        
        btn_logout = QPushButton("🚪 Cerrar Sesión")
        btn_logout.clicked.connect(self.logout)
        
        # Layout de botones
        button_layout = QHBoxLayout()
        button_layout.addWidget(btn_back)
        button_layout.addWidget(btn_save)
        button_layout.addWidget(btn_logout)
        
        # Sección de hora centrada
        time_layout = QHBoxLayout()
        time_layout.addStretch()
        time_layout.addWidget(QLabel("Hora de la comida:"))
        time_layout.addWidget(self.time_edit)
        time_layout.addStretch()
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(lbl_title)
        main_layout.addSpacing(20)
        main_layout.addLayout(grid)
        main_layout.addLayout(time_layout)
        main_layout.addSpacing(30)
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
        
        self.setLayout(main_layout)

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
        
        self.findChild(QLabel).setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #2E7D32;
            padding-bottom: 15px;
        """)

    def save_meal(self):
        """Guarda las comidas en la base de datos"""
        foods = [f.text().strip() for f in self.food_inputs if f.text().strip()]
        
        if not foods:
            QMessageBox.warning(self, "Error", "Debe ingresar al menos un alimento")
            return
            
        time = self.time_edit.time().toString("hh:mm AP")
        hour = self.time_edit.time().hour()
        
        if hour < 12:
            meal_type = "Desayuno"
        elif 12 <= hour < 18:
            meal_type = "Comida"
        else:
            meal_type = "Cena"
        
        success_count = 0
        for food in foods:
            if self.db_manager.add_meal(self.user_id, food, meal_type, time):
                success_count += 1
        
        if success_count > 0:
            QMessageBox.information(
                self, 
                "Éxito", 
                f"Se registraron {success_count} alimentos como {meal_type.lower()}\nHora: {time}"
            )
            
            for field in self.food_inputs:
                field.clear()
            
            self.main_window.load_user_data()
        else:
            QMessageBox.critical(
                self, 
                "Error", 
                "No se pudieron guardar los alimentos. Intente nuevamente"
            )
    
    def go_back_to_dashboard(self):
        """Vuelve a la ventana principal"""
        self.hide()
        self.main_window.show()
    
    def logout(self):
        """Cierra sesión y vuelve al login"""
        self.main_window.logout()