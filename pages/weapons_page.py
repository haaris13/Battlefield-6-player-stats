from PyQt5 import QtWidgets, QtCore

class WeaponsPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)

        self.table = QtWidgets.QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "Arme", "Kills", "Headshots", "Précision (%)",
            "Tirs effectués", "Tirs touchés"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSortingEnabled(True)

        layout.addWidget(self.table)

    def set_data(self, data: dict):
        weapons = data.get("weapons", []) or data.get("weaponStats", [])
        self.table.setRowCount(0)

        for w in weapons:
            row = self.table.rowCount()
            self.table.insertRow(row)

            name = w.get("weaponName", w.get("name", "Inconnu"))
            kills = w.get("kills", "-")
            hs = w.get("headshots", w.get("headshotPercent", "-"))
            acc = w.get("accuracy", "-")
            shots_fired = w.get("shotsFired", "-")
            shots_hit = w.get("shotsHit", "-")

            values = [name, kills, hs, acc, shots_fired, shots_hit]
            for col, val in enumerate(values):
                item = QtWidgets.QTableWidgetItem(str(val))
                if col != 0:
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table.setItem(row, col, item)
