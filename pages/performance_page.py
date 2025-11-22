from PyQt5 import QtWidgets
import json

class PerformancePage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        self.text = QtWidgets.QTextEdit()
        self.text.setReadOnly(True)
        layout.addWidget(self.text)

    def set_data(self, data: dict):
        perf = data.get("performance") or data.get("matches") or data.get("sessions")
        if not perf:
            self.text.setText("Aucune donnée de performance récente fournie par l'API pour ce joueur.")
            return

        if isinstance(perf, list):
            chunks = []
            for match in perf[:10]:
                chunks.append(json.dumps(match, indent=2))
            self.text.setText("\n\n".join(chunks))
        else:
            self.text.setText(json.dumps(perf, indent=2))
