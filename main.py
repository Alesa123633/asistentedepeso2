import sys
from PyQt5.QtWidgets import QApplication
from login_window import LoginWindow

def main():
    app = QApplication(sys.argv)
    
    # Forzar estilo moderno
    app.setStyle('Fusion')
    
    # Crear y mostrar ventana de login
    login = LoginWindow()
    
    # Verificar si el login fue exitoso
    if login.exec_() == LoginWindow.Accepted:
        print("Login exitoso!")
    else:
        print("Login fallido")
        sys.exit(0)

if __name__ == "__main__":
    print("Iniciando aplicación...")
    main()
