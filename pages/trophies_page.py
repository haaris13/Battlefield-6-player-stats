from PyQt5 import QtWidgets

class TrophiesPage(QtWidgets.QWidget):
    """Affiche des objectifs / trophées simples basés sur les stats globales."""
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

        kills = data.get("kills", 0) or 0
        accuracy = data.get("accuracy", 0) or 0
        wins = data.get("wins", 0) or 0
        headshots = data.get("headshots", 0) or 0

        lines = []
        lines.append("=== 🏆 Trophées & objectifs ===")

        if kills >= 10000:
            lines.append("🏅 Maître de la guerre : 10 000 kills ou plus.")
        elif kills >= 5000:
            lines.append("🥇 Tueur confirmé : 5 000 kills ou plus.")
        elif kills >= 1000:
            lines.append("🥈 Soldat expérimenté : 1 000 kills ou plus.")
        else:
            lines.append("🎖️ En progression : vise les 1 000 kills.")

        if isinstance(accuracy, (int, float)):
            if accuracy >= 30:
                lines.append("🎯 Tireur d'élite : précision ≥ 30%.")
            elif accuracy >= 20:
                lines.append("🎯 Tireur confirmé : précision ≥ 20%.")
            else:
                lines.append("🎯 Tireur en progression : vise au moins 20% de précision.")

        if wins >= 500:
            lines.append("🏆 Champion : 500 victoires ou plus.")
        elif wins >= 100:
            lines.append("🏆 Vétéran : 100 victoires ou plus.")
        else:
            lines.append("🏆 Peu de victoires : joue les objectifs pour inverser la tendance.")

        if isinstance(headshots, (int, float)) and headshots > 0:
            lines.append(f"💥 Headshots totaux : {headshots}.")

        lines.append("")
        lines.append("Ces objectifs sont indicatifs, à toi de les adapter à ton style de jeu.")

        self.text.setText("\n".join(lines))
