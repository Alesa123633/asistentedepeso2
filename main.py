import sys
from PyQt5.QtWidgets import QApplication
from login_window import LoginWindow

def main():
    # Configuración de la aplicación
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Estilo moderno
    
    # Crear ventana
    window = LoginWindow()
    
    # Mostrar ventana (usamos show() en lugar de exec_() para mejor depuración)
    window.show()
    
    # Ejecutar aplicación
    sys.exit(app.exec_())

if __name__ == "__main__":
    print("Iniciando aplicación...")  # Mensaje de verificación
    main()
