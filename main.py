import sys
from PyQt5.QtWidgets import QApplication
from login_window import LoginWindow
from food_form import FoodForm

def main():
    app = QApplication(sys.argv)
    
    # Mostrar ventana de login
    login_window = LoginWindow()
    
    if login_window.exec_() == LoginWindow.Accepted:
        # Obtener datos del usuario
        username = login_window.txt_login_user.text()
        user_id = login_window.user_id
        
        # Mostrar ventana de comidas
        food_window = FoodForm(user_id, username)
        food_window.show()  # Mostrar la ventana
        
        # Ejecutar la aplicación
        sys.exit(app.exec_())
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
