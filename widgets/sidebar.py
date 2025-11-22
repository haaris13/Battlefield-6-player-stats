from PyQt5 import QtWidgets, QtCore, QtGui
import os

ICONS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icons")

class Sidebar(QtWidgets.QWidget):
    page_selected = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setFixedWidth(230)
        self.setStyleSheet("""
            QWidget {
                background-color: #0F0F0F;
                color: #EAEAEA;
                font-size: 14px;
            }
            QPushButton {
                background-color: #1A1A1A;
                color: #EAEAEA;
                border-radius: 6px;
                padding: 10px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #2A2A2A;
            }
            QLabel {
                color: #888;
                font-size: 12px;
                font-weight: bold;
                margin-top: 12px;
            }
        """)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)

        title = QtWidgets.QLabel("BF6 Stats Pro")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        layout.addWidget(title)

        layout.addSpacing(10)

        layout.addWidget(self._section("JOUEUR"))
        self._add_btn(layout, "Résumé", "home.png")
        self._add_btn(layout, "Dashboard", "dashboard.png")
        self._add_btn(layout, "Analyse", "analysis.png")
        self._add_btn(layout, "Historique", "history.png")



        layout.addSpacing(8)
        layout.addWidget(self._section("STATS"))
        self._add_btn(layout, "Armes", "weapons.png")
        self._add_btn(layout, "Véhicules", "vehicle.png")

        layout.addSpacing(8)
        layout.addWidget(self._section("AVANCÉ"))
        self._add_btn(layout, "Trophées", "trophy.png")
        self._add_btn(layout, "Comparer", "compare.png")

        layout.addSpacing(8)
        layout.addWidget(self._section("SYSTÈME"))
        self._add_btn(layout, "Favoris", "star.png")
        self._add_btn(layout, "JSON brut", "code.png")

        layout.addStretch()

    def _section(self, text: str):
        return QtWidgets.QLabel(text)

    def _icon(self, filename: str):
        path = os.path.join(ICONS_DIR, filename)
        if os.path.exists(path):
            return QtGui.QIcon(path)
        return QtGui.QIcon()

    def _add_btn(self, layout: QtWidgets.QVBoxLayout, name: str, icon_file: str):
        btn = QtWidgets.QPushButton(f"  {name}")
        btn.setCursor(QtCore.Qt.PointingHandCursor)
        btn.setIcon(self._icon(icon_file))
        btn.setIconSize(QtCore.QSize(20, 20))
        btn.clicked.connect(lambda: self.page_selected.emit(name))
        layout.addWidget(btn)
