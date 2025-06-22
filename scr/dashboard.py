from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel, QLineEdit, 
                            QPushButton, QVBoxLayout, QHBoxLayout, 
                            QMessageBox, QTableWidget, QTableWidgetItem, 
                            QHeaderView, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5.QtGui import QPainter

class Dashboard(QMainWindow):
    logout_requested = pyqtSignal()
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.user_id = None
        self.username = None
        self.food_form = None
        self.setWindowTitle("Dashboard de Nutrición")
        self.setFixedSize(900, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.setup_ui()
        self.setup_styles()

    def setup_ui(self):
        """Configura la interfaz del dashboard"""
        main_layout = QVBoxLayout()
        self.centralWidget().setLayout(main_layout)
        
        # Sección de autenticación (oculta después del login)
        self.auth_layout = QHBoxLayout()
        
        self.lbl_user = QLabel("Usuario:")
        self.txt_user = QLineEdit()
        self.txt_user.setPlaceholderText("Ingrese su usuario")
        
        self.lbl_pass = QLabel("Contraseña:")
        self.txt_pass = QLineEdit()
        self.txt_pass.setEchoMode(QLineEdit.Password)
        self.txt_pass.setPlaceholderText("Ingrese su contraseña")
        
        self.btn_login = QPushButton("Ingresar")
        self.btn_login.clicked.connect(self.authenticate)
        
        self.auth_layout.addWidget(self.lbl_user)
        self.auth_layout.addWidget(self.txt_user)
        self.auth_layout.addWidget(self.lbl_pass)
        self.auth_layout.addWidget(self.txt_pass)
        self.auth_layout.addWidget(self.btn_login)
        
        # Información del usuario
        self.lbl_user_info = QLabel()
        self.lbl_user_info.setAlignment(Qt.AlignCenter)
        
        # Mensaje motivacional
        self.lbl_motivation = QLabel()
        self.lbl_motivation.setAlignment(Qt.AlignCenter)
        self.lbl_motivation.setStyleSheet("font-size: 18px; font-weight: bold; color: #388e3c; padding: 10px;")
        
        # Botones de acciones
        self.action_layout = QHBoxLayout()
        
        self.btn_food_form = QPushButton("🍽️ Registrar Comida")
        self.btn_food_form.clicked.connect(self.open_food_form)
        self.btn_food_form.setEnabled(False)
        
        self.btn_logout = QPushButton("🚪 Cerrar Sesión")
        self.btn_logout.clicked.connect(self.logout)
        self.btn_logout.setEnabled(False)
        
        self.btn_exit = QPushButton("Salir")
        self.btn_exit.clicked.connect(self.logout_requested.emit)
        self.btn_exit.setEnabled(True)
        
        # Botón para borrar alimento
        self.btn_delete_food = QPushButton("🗑️ Borrar Alimento")
        self.btn_delete_food.clicked.connect(self.delete_selected_food)
        self.btn_delete_food.setEnabled(False)
        
        self.action_layout.addWidget(self.btn_food_form)
        self.action_layout.addWidget(self.btn_logout)
        self.action_layout.addWidget(self.btn_exit)
        self.action_layout.addWidget(self.btn_delete_food)
        
        # Gráfico circular
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setMinimumHeight(300)
        
        # Tabla de comidas
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Fecha", "Tipo", "Alimento", "Hora"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setColumnHidden(0, True)  # Oculta la columna de ID

        # Agregar componentes al layout principal
        main_layout.addLayout(self.auth_layout)
        main_layout.addWidget(self.lbl_user_info)
        main_layout.addWidget(self.lbl_motivation)
        main_layout.addLayout(self.action_layout)
        main_layout.addWidget(self.chart_view)
        main_layout.addWidget(self.table)

    def setup_styles(self):
        """Configura los estilos visuales"""
        self.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
                font-family: Arial;
            }
            QLabel {
                font-size: 14px;
                color: #333333;
            }
            QLineEdit {
                font-size: 14px;
                padding: 8px;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                min-width: 150px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 5px;
                border: none;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
            }
            QTableWidget {
                font-size: 14px;
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #2E7D32;
                color: white;
                padding: 8px;
                font-size: 14px;
            }
        """)
        
        self.lbl_user_info.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #1565C0;
            padding: 10px;
            background-color: #E3F2FD;
            border-radius: 5px;
        """)

    def authenticate(self):
        """Valida las credenciales del usuario"""
        username = self.txt_user.text().strip()
        password = self.txt_pass.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Ingrese usuario y contraseña")
            return
        
        success, user_id = self.db_manager.verify_user(username, password)
        
        if success:
            self.user_id = user_id
            self.username = username
            
            # Ocultar campos de login y mostrar información del usuario
            self.lbl_user.hide()
            self.txt_user.hide()
            self.lbl_pass.hide()
            self.txt_pass.hide()
            self.btn_login.hide()
            
            # Mostrar información del usuario y habilitar botones
            self.lbl_user_info.setText(f"Bienvenido: {username} | ID: {user_id}")
            self.btn_food_form.setEnabled(True)
            self.btn_logout.setEnabled(True)
            self.btn_exit.hide()
            self.btn_delete_food.setEnabled(True)
            
            self.load_user_data()
            QMessageBox.information(self, "Éxito", "Autenticación exitosa")
        else:
            QMessageBox.critical(self, "Error", "Credenciales incorrectas")
            self.reset_ui()

    def load_user_data(self):
        """Carga los datos específicos del usuario"""
        meal_data, meals = self.db_manager.get_user_meals(self.user_id)
        
        # --- Análisis de alimentos para mensaje motivacional ---
        healthy_keywords = ["manzana", "lechuga", "ensalada", "zanahoria", "pepino", "pollo asado", "pescado", "fruta", "verdura", "avena", "yogur", "plátano", "pera", "espinaca", "brócoli", "naranja", "agua"]
        junk_keywords = ["refresco", "pizza", "hamburguesa", "papas", "fritura", "hot dog", "pan dulce", "galleta", "pastel", "dulce", "chocolate", "tamal", "torta", "soda", "chatarra", "empanizado", "frito", "nugget", "helado", "panque", "panqué", "pan", "donas", "papas a la francesa"]
        found_healthy = False
        found_junk = False
        for meal in meals:
            food_name = meal[3].lower()
            if any(word in food_name for word in healthy_keywords):
                found_healthy = True
            if any(word in food_name for word in junk_keywords):
                found_junk = True
        if meals:
            if found_junk:
                self.lbl_motivation.setStyleSheet("font-size: 18px; font-weight: bold; color: #c62828; padding: 10px;")
                self.lbl_motivation.setText("Come cosas nutritivas como manzana, lechuga, ensalada, etc.\nEvita comidas tipo dieta: pizza, hamburguesa, papas, refresco, pan dulce, etc.")
            elif found_healthy:
                self.lbl_motivation.setStyleSheet("font-size: 18px; font-weight: bold; color: #388e3c; padding: 10px;")
                self.lbl_motivation.setText("¡Muy bien! Aquí te dejo unas recomendaciones:\n- Mantén variedad de frutas y verduras\n- Prefiere agua sobre refrescos\n- Incluye proteínas magras\n- Evita exceso de azúcares y frituras\n- Haz ejercicio regularmente")
            else:
                self.lbl_motivation.setText("")
        else:
            self.lbl_motivation.setText("")
        
        if meal_data is not None:
            # Crear gráfico circular
            series = QPieSeries()
            for meal_type, count in meal_data:
                slice_ = series.append(f"{meal_type} ({count})", count)
                slice_.setLabelVisible(True)
            
            chart = QChart()
            chart.addSeries(series)
            chart.setTitle(f"Distribución de Comidas - {self.username}")
            chart.setAnimationOptions(QChart.SeriesAnimations)
            self.chart_view.setChart(chart)
            
            # Llenar tabla
            self.table.setRowCount(len(meals))
            for row, meal in enumerate(meals):
                # meal debe incluir el ID ahora
                if len(meal) == 5:
                    meal_id, fecha, meal_type, food_name, time = meal
                else:
                    # Compatibilidad por si get_user_meals no devuelve el ID aún
                    meal_id = None
                    fecha, meal_type, food_name, time = meal
                self.table.setItem(row, 0, QTableWidgetItem(str(meal_id) if meal_id else ""))
                self.table.setItem(row, 1, QTableWidgetItem(fecha))
                self.table.setItem(row, 2, QTableWidgetItem(meal_type))
                self.table.setItem(row, 3, QTableWidgetItem(food_name))
                self.table.setItem(row, 4, QTableWidgetItem(time))

    def open_food_form(self):
        """Abre el formulario de registro de comidas"""
        from food_form import FoodForm
        if self.food_form is None:
            self.food_form = FoodForm(self.user_id, self.username, self.db_manager, self)
        
        self.hide()
        self.food_form.show()

    def logout(self):
        """Cierra la sesión del usuario"""
        self.reset_ui()
        self.lbl_user.show()
        self.txt_user.show()
        self.txt_user.clear()
        self.lbl_pass.show()
        self.txt_pass.show()
        self.txt_pass.clear()
        self.btn_login.show()
        self.logout_requested.emit()
        QMessageBox.information(self, "Sesión", "Has cerrado sesión correctamente")

    def reset_ui(self):
        """Restablece la interfaz"""
        self.user_id = None
        self.username = None
        self.lbl_user_info.setText("")
        self.lbl_motivation.setText("")
        self.chart_view.setChart(QChart())
        self.table.setRowCount(0)
        self.btn_food_form.setEnabled(False)
        self.btn_logout.setEnabled(False)
        self.btn_exit.show()
        self.btn_delete_food.setEnabled(False)
        
        if self.food_form:
            self.food_form.close()
            self.food_form = None

    def delete_selected_food(self):
        """Borra todos los alimentos seleccionados en la tabla"""
        selected_rows = set([index.row() for index in self.table.selectedIndexes()])
        if not selected_rows:
            QMessageBox.warning(self, "Error", "Seleccione al menos un alimento para borrar.")
            return
        meal_ids = []
        for row in selected_rows:
            meal_id_item = self.table.item(row, 0)
            if meal_id_item and meal_id_item.text():
                meal_ids.append(int(meal_id_item.text()))
        if not meal_ids:
            QMessageBox.warning(self, "Error", "No se pueden identificar los alimentos a borrar.")
            return
        confirm = QMessageBox.question(self, "Confirmar", f"¿Está seguro de que desea borrar {len(meal_ids)} alimento(s)?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            success_count = 0
            for meal_id in meal_ids:
                if self.db_manager.delete_meal(meal_id):
                    success_count += 1
            if success_count == len(meal_ids):
                QMessageBox.information(self, "Éxito", f"Se borraron {success_count} alimento(s) correctamente.")
            else:
                QMessageBox.warning(self, "Advertencia", f"Solo se borraron {success_count} de {len(meal_ids)} alimento(s).")
            self.load_user_data()