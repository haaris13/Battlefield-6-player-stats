from PyQt5 import QtWidgets
import json

class ObjectivesPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        self.text = QtWidgets.QTextEdit()
        self.text.setReadOnly(True)
        layout.addWidget(self.text)

    def set_data(self, data: dict):
        objectives = data.get("objectives") or data.get("objectiveStats")
        if not objectives:
            self.text.setText("L'API ne renvoie pas (encore) de stats d'objectifs détaillées pour ce joueur.")
            return

        if isinstance(objectives, dict):
            lines = []
            for k, v in objectives.items():
                lines.append(f"{k} : {v}")
            self.text.setText("\n".join(lines))
        else:
            self.text.setText(json.dumps(objectives, indent=2))
