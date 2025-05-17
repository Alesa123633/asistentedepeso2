from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTimeEdit, QMessageBox, QGridLayout
from PyQt5.QtCore import QTime

class FoodForm(QWidget):
    def __init__(self, user_id, username):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle(f"Dieta de {username}")
        self.setFixedSize(600, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Campos para alimentos
        self.food_inputs = []
        grid = QGridLayout()
        for i in range(5):
            label = QLabel(f"Alimento {i+1}:")
            input_field = QLineEdit()
            self.food_inputs.append(input_field)
            grid.addWidget(label, i, 0)
            grid.addWidget(input_field, i, 1)

        # Selector de hora
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("hh:mm AP")
        self.time_edit.setTime(QTime.currentTime())
        grid.addWidget(QLabel("Hora:"), 5, 0)
        grid.addWidget(self.time_edit, 5, 1)

        # Botón de guardar
        save_btn = QPushButton("Guardar Comida")
        save_btn.clicked.connect(self.save_meal)
        grid.addWidget(save_btn, 6, 0, 1, 2)

        layout.addLayout(grid)
        self.setLayout(layout)

    def save_meal(self):
        from database import create_connection
        foods = [f.text() for f in self.food_inputs if f.text().strip()]
        
        if not foods:
            QMessageBox.warning(self, "Error", "Ingresa al menos un alimento")
            return
            
        time = self.time_edit.time().toString("hh:mm")
        hour = self.time_edit.time().hour()
        meal_type = "Desayuno" if hour < 12 else "Comida" if hour < 18 else "Cena"
        
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                for food in foods:
                    cursor.execute('''
                        INSERT INTO meals (user_id, food, meal_type, time)
                        VALUES (?, ?, ?, ?)
                    ''', (self.user_id, food, meal_type, time))
                conn.commit()
                QMessageBox.information(self, "Éxito", "Comida registrada")
                for field in self.food_inputs:
                    field.clear()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
            finally:
                conn.close()