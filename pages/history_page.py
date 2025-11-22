from PyQt5 import QtWidgets, QtCore
import json
import os

HISTORY_FILE = "history.json"

class HistoryPage(QtWidgets.QWidget):
    """Affiche un historique simple des stats globales enregistrées localement."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)

        self.table = QtWidgets.QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "Joueur", "Plateforme", "Kills", "Morts", "K/D", "Score/min"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        layout.addWidget(self.table)

        self.load_history()

    def load_history(self):
        self.table.setRowCount(0)
        if not os.path.exists(HISTORY_FILE):
            return
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                entries = json.load(f)
        except Exception:
            return
        for entry in entries[-50:]:
            row = self.table.rowCount()
            self.table.insertRow(row)
            vals = [
                entry.get("userName", "?"),
                entry.get("platform", "?"),
                entry.get("kills", "-"),
                entry.get("deaths", "-"),
                entry.get("kd", "-"),
                entry.get("spm", "-"),
            ]
            for col, val in enumerate(vals):
                item = QtWidgets.QTableWidgetItem(str(val))
                if col >= 2:
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table.setItem(row, col, item)

    def add_entry(self, snapshot: dict):
        data = []
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = []
        data.append(snapshot)
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
        self.load_history()
