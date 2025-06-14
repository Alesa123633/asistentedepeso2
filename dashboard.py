from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel, QLineEdit, 
                            QPushButton, QVBoxLayout, QHBoxLayout, 
                            QMessageBox, QTableWidget, QTableWidgetItem, 
                            QHeaderView, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5.QtGui import QPainter

class Dashboard(QMainWindow):
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
        
        # Botones de acciones
        self.action_layout = QHBoxLayout()
        
        self.btn_food_form = QPushButton("🍽️ Registrar Comida")
        self.btn_food_form.clicked.connect(self.open_food_form)
        self.btn_food_form.setEnabled(False)
        
        self.btn_logout = QPushButton("🚪 Cerrar Sesión")
        self.btn_logout.clicked.connect(self.logout)
        self.btn_logout.setEnabled(False)
        
        self.action_layout.addWidget(self.btn_food_form)
        self.action_layout.addWidget(self.btn_logout)
        
        # Gráfico circular
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setMinimumHeight(300)
        
        # Tabla de comidas
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Fecha", "Tipo", "Alimento", "Hora"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Agregar componentes al layout principal
        main_layout.addLayout(self.auth_layout)
        main_layout.addWidget(self.lbl_user_info)
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
            
            self.load_user_data()
            QMessageBox.information(self, "Éxito", "Autenticación exitosa")
        else:
            QMessageBox.critical(self, "Error", "Credenciales incorrectas")
            self.reset_ui()

    def load_user_data(self):
        """Carga los datos específicos del usuario"""
        meal_data, meals = self.db_manager.get_user_meals(self.user_id)
        
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
            for row, (fecha, meal_type, food_name, time) in enumerate(meals):
                self.table.setItem(row, 0, QTableWidgetItem(fecha))
                self.table.setItem(row, 1, QTableWidgetItem(meal_type))
                self.table.setItem(row, 2, QTableWidgetItem(food_name))
                self.table.setItem(row, 3, QTableWidgetItem(time))

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
        QMessageBox.information(self, "Sesión", "Has cerrado sesión correctamente")

    def reset_ui(self):
        """Restablece la interfaz"""
        self.user_id = None
        self.username = None
        self.lbl_user_info.setText("")
        self.chart_view.setChart(QChart())
        self.table.setRowCount(0)
        self.btn_food_form.setEnabled(False)
        self.btn_logout.setEnabled(False)
        
        if self.food_form:
            self.food_form.close()
            self.food_form = None
