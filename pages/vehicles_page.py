from PyQt5 import QtWidgets, QtCore

class VehiclesPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)

        self.table = QtWidgets.QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Véhicule", "Kills", "Temps d'utilisation"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSortingEnabled(True)

        layout.addWidget(self.table)

    def _fmt_time(self, value):
        try:
            sec = int(value)
        except Exception:
            return str(value) if value not in (None, "") else "-"
        h = sec // 3600
        m = (sec % 3600) // 60
        return f"{h}h {m:02d}m"

    def set_data(self, data: dict):
        vehicles = data.get("vehicles", []) or data.get("vehicleStats", [])
        self.table.setRowCount(0)

        for v in vehicles:
            row = self.table.rowCount()
            self.table.insertRow(row)

            name = v.get("vehicleName", v.get("name", "Inconnu"))
            kills = v.get("kills", "-")
            time_raw = v.get("timeUsed") or v.get("timePlayed") or v.get("secondsPlayed")
            time_str = self._fmt_time(time_raw) if time_raw is not None else "-"

            values = [name, kills, time_str]
            for col, val in enumerate(values):
                item = QtWidgets.QTableWidgetItem(str(val))
                if col != 0:
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table.setItem(row, col, item)
