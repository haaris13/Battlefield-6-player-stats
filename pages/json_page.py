from PyQt5 import QtWidgets
import json

class JsonPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        self.text = QtWidgets.QTextEdit()
        self.text.setReadOnly(True)
        layout.addWidget(self.text)

    def set_data(self, data: dict):
        if not data:
            self.text.setText("Aucune donnée.")
            return
        try:
            self.text.setText(json.dumps(data, indent=2))
        except Exception:
            self.text.setText(str(data))
