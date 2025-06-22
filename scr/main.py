import sys
from PyQt5.QtWidgets import QApplication
from database import DatabaseManager
from login_window import LoginWindow
from dashboard import Dashboard
from appcontroller import ApplicationController

class NutritionApp:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.app = QApplication(sys.argv)
        
        # Primero mostramos el login
        self.login_window = LoginWindow(self.db_manager)
        
        # Luego el dashboard
        self.dashboard = Dashboard(self.db_manager)
        
        # Conectamos las señales
        self.login_window.accepted.connect(self.show_dashboard)
    
    def show_dashboard(self):
        """Muestra el dashboard después del login exitoso"""
        self.dashboard.user_id = self.login_window.user_id
        self.dashboard.username = self.login_window.txt_login_user.text()
        self.dashboard.authenticate()
        self.dashboard.show()
    
    def run(self):
        """Ejecuta la aplicación"""
        self.login_window.show()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app_controller = ApplicationController()
    app_controller.run()