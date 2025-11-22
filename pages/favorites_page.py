from PyQt5 import QtWidgets
import json
import os

FAVORITES_FILE = "favorites.json"

class FavoritesPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_player = None
        self.current_platform = None
        self.init_ui()
        self.load_favorites()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        top = QtWidgets.QHBoxLayout()
        self.btn_add = QtWidgets.QPushButton("Ajouter le joueur courant aux favoris")
        self.btn_remove = QtWidgets.QPushButton("Supprimer le favori sélectionné")
        top.addWidget(self.btn_add)
        top.addWidget(self.btn_remove)
        layout.addLayout(top)

        self.list = QtWidgets.QListWidget()
        layout.addWidget(self.list)

        self.btn_add.clicked.connect(self.add_current)
        self.btn_remove.clicked.connect(self.remove_selected)

    def set_current_player(self, name: str, platform: str):
        self.current_player = name
        self.current_platform = platform

    def load_favorites(self):
        self.list.clear()
        if not os.path.exists(FAVORITES_FILE):
            return
        try:
            with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
                favs = json.load(f)
            for entry in favs:
                self.list.addItem(f"{entry['name']} ({entry['platform']})")
        except Exception:
            pass

    def save_favorites(self):
        favs = []
        for i in range(self.list.count()):
            text = self.list.item(i).text()
            if "(" in text and text.endswith(")"):
                name, rest = text.split("(", 1)
                name = name.strip()
                platform = rest[:-1].strip()
                favs.append({"name": name, "platform": platform})
        try:
            with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
                json.dump(favs, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def add_current(self):
        if not self.current_player or not self.current_platform:
            QtWidgets.QMessageBox.warning(self, "Info", "Aucun joueur courant défini.")
            return
        item_text = f"{self.current_player} ({self.current_platform})"
        for i in range(self.list.count()):
            if self.list.item(i).text() == item_text:
                return
        self.list.addItem(item_text)
        self.save_favorites()

    def remove_selected(self):
        row = self.list.currentRow()
        if row < 0:
            return
        self.list.takeItem(row)
        self.save_favorites()
