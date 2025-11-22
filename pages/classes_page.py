from PyQt5 import QtWidgets, QtCore

class ClassesPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)

        self.table = QtWidgets.QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Classe", "Temps joué", "Score/min", "Kills"])
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
        classes = data.get("classes", []) or data.get("classStats", [])
        self.table.setRowCount(0)

        for c in classes:
            row = self.table.rowCount()
            self.table.insertRow(row)

            name = c.get("className", c.get("name", "?"))
            time_raw = c.get("timePlayed") or c.get("secondsPlayed") or c.get("timeUsed")
            time_str = self._fmt_time(time_raw) if time_raw is not None else "-"
            spm = c.get("spm") or c.get("scorePerMinute") or "-"
            kills = c.get("kills", "-")

            values = [name, time_str, spm, kills]
            for col, val in enumerate(values):
                item = QtWidgets.QTableWidgetItem(str(val))
                if col != 0:
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table.setItem(row, col, item)
