from PyQt5 import QtWidgets, QtCore
from api import fetch_stats

class ComparePage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        form = QtWidgets.QHBoxLayout()
        self.input_player1 = QtWidgets.QLineEdit()
        self.input_player1.setPlaceholderText("Joueur 1")
        self.input_player2 = QtWidgets.QLineEdit()
        self.input_player2.setPlaceholderText("Joueur 2")

        self.platform_combo = QtWidgets.QComboBox()
        self.platform_combo.addItems(["pc", "ps", "xbox"])

        btn = QtWidgets.QPushButton("Comparer")
        btn.clicked.connect(self.on_compare)

        form.addWidget(self.input_player1)
        form.addWidget(self.input_player2)
        form.addWidget(self.platform_combo)
        form.addWidget(btn)

        layout.addLayout(form)

        self.result = QtWidgets.QTextEdit()
        self.result.setReadOnly(True)
        layout.addWidget(self.result)

    def _extract_summary(self, data: dict):
        if not data:
            return None
        kills = data.get("kills", 0) or 0
        deaths = data.get("deaths", 0) or 0
        accuracy = data.get("accuracy", 0) or 0
        kpm = data.get("kpm") or data.get("killsPerMinute") or 0
        spm = data.get("spm") or data.get("scorePerMinute") or 0

        kd = "-"
        if isinstance(kills, (int, float)) and isinstance(deaths, (int, float)) and deaths > 0:
            kd = round(kills / deaths, 2)

        return {
            "name": data.get("userName", "?"),
            "kills": kills,
            "deaths": deaths,
            "kd": kd,
            "accuracy": accuracy,
            "kpm": kpm,
            "spm": spm,
        }

    def on_compare(self):
        p1 = self.input_player1.text().strip()
        p2 = self.input_player2.text().strip()
        platform = self.platform_combo.currentText()

        if not p1 or not p2:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Veuillez entrer deux joueurs.")
            return

        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        d1 = fetch_stats(p1, platform)
        d2 = fetch_stats(p2, platform)
        QtWidgets.QApplication.restoreOverrideCursor()

        if not d1 or not d2:
            self.result.setText("Impossible de récupérer les stats pour l'un des joueurs.")
            return

        s1 = self._extract_summary(d1)
        s2 = self._extract_summary(d2)

        lines = []
        lines.append(f"Comparaison ({platform})")
        lines.append("")
        lines.append(f"{s1['name']}  VS  {s2['name']}")
        lines.append("")
        lines.append(f"Kills : {s1['kills']}  /  {s2['kills']}")
        lines.append(f"Morts : {s1['deaths']}  /  {s2['deaths']}")
        lines.append(f"K/D : {s1['kd']}  /  {s2['kd']}")
        lines.append(f"Précision : {s1['accuracy']}%  /  {s2['accuracy']}%")
        lines.append(f"Kills/min : {s1['kpm']}  /  {s2['kpm']}")
        lines.append(f"Score/min : {s1['spm']}  /  {s2['spm']}")

        self.result.setText("\n".join(lines))
