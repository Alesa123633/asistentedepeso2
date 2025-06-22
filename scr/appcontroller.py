from PyQt5.QtWidgets import QApplication
import sys
import os

# Asegurar que las importaciones locales funcionen
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from login_window import LoginWindow
    from dashboard import Dashboard
    from database import DatabaseManager
except ImportError as e:
    print(f"Error de importación: {e}")
    raise

class ApplicationController:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.app = QApplication(sys.argv)
        
        # Crear instancias
        self.login_window = LoginWindow(self.db_manager)
        self.dashboard = Dashboard(self.db_manager)
        
        # Conectar señales - IMPORTANTE: hacerlo después de crear ambas instancias
        self.dashboard.logout_requested.connect(self.show_login)
        self.login_window.accepted.connect(self.show_dashboard)
        
    def show_dashboard(self):
        self.dashboard.user_id = self.login_window.user_id
        self.dashboard.username = self.login_window.txt_login_user.text()
        self.dashboard.authenticate()
        self.dashboard.show()
        self.login_window.hide()
        
    def show_login(self):
        self.login_window.txt_login_user.clear()
        self.login_window.txt_login_pass.clear()
        self.login_window.show()
        self.dashboard.hide()
        
    def run(self):
        self.login_window.show()
        sys.exit(self.app.exec_())

# Para pruebas directas
if __name__ == "__main__":
    controller = ApplicationController()
    controller.run()
    