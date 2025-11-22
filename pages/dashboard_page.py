from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class DashboardPage(QtWidgets.QWidget):
    """Dashboard avec quelques graphiques (armes + classes + kills global)."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        self.info_label = QtWidgets.QLabel("")
        layout.addWidget(self.info_label)

    def set_data(self, data: dict):
        self.fig.clear()

        weapons = data.get("weapons", []) or data.get("weaponStats", [])
        classes = data.get("classes", []) or data.get("classStats", [])
        kills = data.get("kills", 0) or 0
        deaths = data.get("deaths", 0) or 0

        has_any = False

        if weapons:
            has_any = True
            ax1 = self.fig.add_subplot(131)
            sorted_weapons = sorted(weapons, key=lambda w: w.get("kills", 0) or 0, reverse=True)[:5]
            names = [w.get("weaponName", w.get("name", "?")) for w in sorted_weapons]
            vals = [w.get("kills", 0) or 0 for w in sorted_weapons]
            ax1.bar(names, vals)
            ax1.set_title("Top 5 armes (kills)")
            ax1.tick_params(axis='x', rotation=45)

        if classes:
            has_any = True
            ax2 = self.fig.add_subplot(132)
            labels = []
            vals = []
            for c in classes:
                name = c.get("className", c.get("name", "?"))
                t = c.get("timePlayed") or c.get("secondsPlayed") or 0
                try:
                    t = int(t)
                except Exception:
                    t = 0
                if t > 0:
                    labels.append(name)
                    vals.append(t / 3600.0)
            if labels and vals:
                ax2.bar(labels, vals)
                ax2.set_title("Temps par classe (heures)")
                ax2.tick_params(axis='x', rotation=45)

        if isinstance(kills, (int, float)) and isinstance(deaths, (int, float)) and (kills > 0 or deaths > 0):
            has_any = True
            ax3 = self.fig.add_subplot(133)
            ax3.bar(["Kills", "Morts"], [kills, deaths])
            ax3.set_title("Kills vs Morts")

        if has_any:
            self.info_label.setText("Graphiques basés sur les armes, classes et kills globaux.")
        else:
            self.info_label.setText("Pas assez de données pour afficher des graphiques.")
        self.fig.tight_layout()
        self.canvas.draw()
