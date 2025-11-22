import sys
from PyQt5 import QtWidgets
from ui_main import MainWindow
from license_check import ensure_license   # <--- IMPORTANT

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # 💳 Vérification de la licence AVANT de lancer l'app
    if not ensure_license():
        sys.exit(0)

    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
