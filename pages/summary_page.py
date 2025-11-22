from PyQt5 import QtWidgets

class SummaryPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        self.text = QtWidgets.QTextEdit()
        self.text.setReadOnly(True)
        layout.addWidget(self.text)

    def set_data(self, data: dict):
        if not data:
            self.text.setText("Aucune donnée à afficher.")
            return

        def get_any(*names, default="-"):
            for n in names:
                if n in data and data[n] not in (None, "", []):
                    return data[n]
            return default

        kills = data.get("kills")
        deaths = data.get("deaths")

        raw_kd = get_any("kd", "kdRatio", default=None)
        if raw_kd not in (None, "-"):
            kd_display = raw_kd
        else:
            if isinstance(kills, (int, float)) and isinstance(deaths, (int, float)) and deaths > 0:
                kd_display = round(kills / deaths, 2)
            else:
                kd_display = "-"

        wins = data.get("wins")
        losses = data.get("losses")
        if losses is None:
            matches = get_any("matchesPlayed", "roundsPlayed", default=None)
            try:
                if matches is not None and wins is not None:
                    losses = int(matches) - int(wins)
            except Exception:
                losses = None

        accuracy = get_any("accuracy", default='-')
        kpm = get_any("kpm", "killsPerMinute", default='-')
        spm = get_any("spm", "scorePerMinute", default='-')

        power_score = "-"
        try:
            kd_val = float(kd_display) if kd_display not in ("-", None) else 0
            acc_val = float(accuracy) if accuracy not in ("-", None) else 0
            kpm_val = float(kpm) if kpm not in ("-", None) else 0
            spm_val = float(spm) if spm not in ("-", None) else 0
            score = 0
            score += min(kd_val / 3 * 30, 30)
            score += min(acc_val / 30 * 20, 20)
            score += min(kpm_val / 2 * 25, 25)
            score += min(spm_val / 1000 * 25, 25)
            power_score = round(min(score, 100), 1)
        except Exception:
            power_score = "-"

        lines = []
        lines.append(f"🎮 Joueur : {get_any('userName')}")
        lines.append(f"💻 Plateforme : {get_any('platform')}")
        lines.append("")
        lines.append("=== 📊 Statistiques générales ===")
        lines.append(f"🔫 Kills : {kills if kills is not None else '-'}")
        lines.append(f"💀 Morts : {deaths if deaths is not None else '-'}")
        lines.append(f"⚔️ Ratio K/D : {kd_display}")
        lines.append(f"🏆 Victoires : {wins if wins is not None else '-'}")
        lines.append(f"❌ Défaites : {losses if losses is not None else '-'}")
        lines.append(f"🎯 Précision : {accuracy}%")
        lines.append("")
        lines.append("=== 🕹️ Autres infos ===")
        lines.append(f"⏳ Temps joué : {get_any('timePlayed', 'time_played')}")
        lines.append(f"📈 Score total : {get_any('score', 'totalScore')}")
        lines.append(f"📊 Score / minute : {spm}")
        lines.append(f"🔫 Kills / minute : {kpm}")
        lines.append(f"🚀 Headshots : {get_any('headshotPercent', 'headshots')}%")
        lines.append(f"🔫 Tirs effectués : {get_any('shotsFired', 'shots')}")
        lines.append(f"🎯 Tirs touchés : {get_any('shotsHit', 'hits')}")
        lines.append("")
        lines.append("=== 💥 Score de puissance BF6 (0-100) ===")
        lines.append(f"⭐ Score : {power_score}")

        self.text.setText("\n".join(lines))
