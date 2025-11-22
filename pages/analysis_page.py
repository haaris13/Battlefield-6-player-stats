from PyQt5 import QtWidgets

class AnalysisPage(QtWidgets.QWidget):
    """Analyse du style de jeu et recommandations simples basées sur les stats."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        self.text = QtWidgets.QTextEdit()
        self.text.setReadOnly(True)
        layout.addWidget(self.text)

    def set_data(self, data: dict):
        if not data:
            self.text.setText("Aucune donnée à analyser.")
            return

        lines = []

        kills = data.get("kills", 0) or 0
        deaths = data.get("deaths", 0) or 0
        accuracy = data.get("accuracy", 0) or 0
        kpm = data.get("kpm") or data.get("killsPerMinute") or 0
        spm = data.get("spm") or data.get("scorePerMinute") or 0
        vehicles = data.get("vehicles", []) or data.get("vehicleStats", [])
        classes = data.get("classes", []) or data.get("classStats", [])

        kd = None
        if isinstance(kills, (int, float)) and isinstance(deaths, (int, float)) and deaths > 0:
            kd = kills / deaths

        lines.append("=== 🔍 Analyse du style de jeu ===")
        if kd is not None:
            if kd >= 2:
                lines.append("• Tu as un excellent K/D : joueur très agressif et efficace en duel.")
            elif kd >= 1:
                lines.append("• Ton K/D est correct : style équilibré entre agressivité et survie.")
            else:
                lines.append("• Ton K/D est en dessous de 1 : tu prends peut-être trop de risques ou meurs souvent hors de position.")

        if isinstance(accuracy, (int, float)):
            if accuracy >= 30:
                lines.append("• Très bonne précision : idéal pour fusils d'assaut / DMR / sniper.")
            elif accuracy >= 20:
                lines.append("• Précision correcte : tu peux encore progresser en contrôlant mieux le recul.")
            else:
                lines.append("• Précision faible : privilégie les rafales courtes et combats à moyenne distance.")

        if isinstance(kpm, (int, float)):
            if kpm >= 1:
                lines.append("• Beaucoup de kills par minute : tu es très présent dans les combats.")
            elif kpm >= 0.5:
                lines.append("• Kills/min dans la moyenne : style de jeu plutôt équilibré.")
            else:
                lines.append("• Peu de kills/min : peut-être sniper, support ou jeu très prudent.")

        if isinstance(spm, (int, float)):
            if spm >= 400:
                lines.append("• Score/min élevé : tu joues bien les objectifs et aides ton équipe.")
            elif spm >= 200:
                lines.append("• Score/min correct : tu participes globalement aux objectifs.")
            else:
                lines.append("• Score/min faible : capture plus de points, réanime, donne des munitions, etc.")

        if vehicles:
            lines.append("")
            lines.append("=== 🚗 Profil véhicule ===")
            total_veh_kills = sum(v.get("kills", 0) or 0 for v in vehicles)
            if total_veh_kills > 0 and kills:
                ratio = total_veh_kills / kills
                if ratio > 0.5:
                    lines.append("• Une grande partie de tes kills vient des véhicules : joueur orienté véhicule.")
                elif ratio > 0.2:
                    lines.append("• Tu utilises régulièrement les véhicules avec impact.")
                else:
                    lines.append("• Tu joues surtout l'infanterie, les véhicules sont secondaires.")
            else:
                lines.append("• Quasi aucune donnée véhicule : tu es principalement infanterie.")

        if classes:
            lines.append("")
            lines.append("=== 👥 Profil des classes ===")
            best_class = None
            best_time = 0
            for c in classes:
                name = c.get("className", c.get("name", "?"))
                t = c.get("timePlayed") or c.get("secondsPlayed") or 0
                try:
                    t = int(t)
                except Exception:
                    t = 0
                if t > best_time:
                    best_time = t
                    best_class = name
            if best_class:
                lines.append(f"• Classe la plus jouée : {best_class}.")
                lower = best_class.lower()
                if "assault" in lower:
                    lines.append("  → Tu joues beaucoup l'assaut, souvent en première ligne.")
                elif "support" in lower:
                    lines.append("  → Tu joues le soutien, utile pour munitions et soins.")
                elif "recon" in lower or "sniper" in lower:
                    lines.append("  → Tu joues souvent en distance, profil sniper / reconnaissance.")
                elif "engineer" in lower:
                    lines.append("  → Tu joues l'ingénieur, efficace contre les véhicules.")

        lines.append("")
        lines.append("=== 💡 Pistes d'amélioration générales ===")
        lines.append("• Joue plus les objectifs (captures, défenses, réanimations) pour augmenter ton SPM.")
        lines.append("• Utilise davantage l'arme avec laquelle tu as la meilleure précision.")
        lines.append("• Surveille l'évolution de ton K/D et de ton Score/min au fil du temps pour voir ta progression.")

        self.text.setText("\n".join(lines))
