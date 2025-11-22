from PyQt5 import QtWidgets, QtCore
from widgets.sidebar import Sidebar
from pages.summary_page import SummaryPage
from pages.weapons_page import WeaponsPage
from pages.vehicles_page import VehiclesPage
from pages.classes_page import ClassesPage
from pages.objectives_page import ObjectivesPage
from pages.performance_page import PerformancePage
from pages.compare_page import ComparePage
from pages.favorites_page import FavoritesPage
from pages.json_page import JsonPage
from pages.analysis_page import AnalysisPage
from pages.dashboard_page import DashboardPage
from pages.trophies_page import TrophiesPage
from pages.history_page import HistoryPage
from api import fetch_stats

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.data = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Battlefield 6 — BF6 Stats Pro v2")
        self.resize(1366, 820)

        self.setStyleSheet("""
            QWidget { background-color: #121212; color: #E0E0E0; font-size: 14px; }
            QLineEdit, QComboBox {
                background-color: #1E1E1E;
                border: 1px solid #333;
                border-radius: 6px;
                padding: 6px;
                color: white;
            }
            QPushButton {
                background-color: #2E7D32;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
            QTableWidget {
                background-color: #1E1E1E;
                gridline-color: #333;
            }
            QHeaderView::section {
                background-color: #212121;
                color: #E0E0E0;
                padding: 5px;
            }
            QTextEdit {
                background-color: #1E1E1E;
                border: 1px solid #333;
                padding: 10px;
                border-radius: 6px;
            }
        """)

        root = QtWidgets.QHBoxLayout(self)

        self.sidebar = Sidebar()
        self.sidebar.page_selected.connect(self.switch_page)
        root.addWidget(self.sidebar)

        right = QtWidgets.QVBoxLayout()

        search_layout = QtWidgets.QHBoxLayout()
        self.input_player = QtWidgets.QLineEdit()
        self.input_player.setPlaceholderText("Nom du joueur (EA / Gamertag)")
        self.input_player.returnPressed.connect(self.on_search)

        self.platform_combo = QtWidgets.QComboBox()
        self.platform_combo.addItems(["pc", "ps", "xbox"])

        btn_search = QtWidgets.QPushButton("Rechercher")
        btn_search.clicked.connect(self.on_search)

        search_layout.addWidget(self.input_player)
        search_layout.addWidget(self.platform_combo)
        search_layout.addWidget(btn_search)

        right.addLayout(search_layout)

        self.stack = QtWidgets.QStackedWidget()
        right.addWidget(self.stack)

        self.page_summary = SummaryPage()
        self.page_dashboard = DashboardPage()
        self.page_analysis = AnalysisPage()
        self.page_history = HistoryPage()
        self.page_weapons = WeaponsPage()
        self.page_vehicles = VehiclesPage()
        self.page_classes = ClassesPage()
        self.page_objectives = ObjectivesPage()
        self.page_performance = PerformancePage()
        self.page_trophies = TrophiesPage()
        self.page_compare = ComparePage()
        self.page_favorites = FavoritesPage()
        self.page_json = JsonPage()

        for page in [
            self.page_summary, self.page_dashboard, self.page_analysis, self.page_history,
            self.page_weapons, self.page_vehicles, self.page_classes,
            self.page_objectives, self.page_performance, self.page_trophies,
            self.page_compare, self.page_favorites, self.page_json
        ]:
            self.stack.addWidget(page)

        root.addLayout(right, 1)

    def switch_page(self, name: str):
        mapping = {
            "Résumé": self.page_summary,
            "Dashboard": self.page_dashboard,
            "Analyse": self.page_analysis,
            "Historique": self.page_history,
            "Armes": self.page_weapons,
            "Véhicules": self.page_vehicles,
            "Classes": self.page_classes,
            "Objectifs": self.page_objectives,
            "Performance": self.page_performance,
            "Trophées": self.page_trophies,
            "Comparer": self.page_compare,
            "Favoris": self.page_favorites,
            "JSON brut": self.page_json,
        }
        page = mapping.get(name)
        if page is not None:
            index = self.stack.indexOf(page)
            if index != -1:
                self.stack.setCurrentIndex(index)

    def on_search(self):
        player = self.input_player.text().strip()
        platform = self.platform_combo.currentText()

        if not player:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Veuillez entrer un nom de joueur.")
            return

        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        data = fetch_stats(player, platform)
        QtWidgets.QApplication.restoreOverrideCursor()

        if not data:
            QtWidgets.QMessageBox.critical(self, "Erreur", "Impossible de récupérer les stats.")
            return

        self.data = data
        self.update_pages()

    def update_pages(self):
        if not self.data:
            return
        self.page_summary.set_data(self.data)
        self.page_dashboard.set_data(self.data)
        self.page_analysis.set_data(self.data)
        self.page_weapons.set_data(self.data)
        self.page_vehicles.set_data(self.data)
        self.page_classes.set_data(self.data)
        self.page_objectives.set_data(self.data)
        self.page_performance.set_data(self.data)
        self.page_trophies.set_data(self.data)
        self.page_json.set_data(self.data)

        snapshot = {
            "userName": self.data.get("userName"),
            "platform": self.data.get("platform"),
            "kills": self.data.get("kills"),
            "deaths": self.data.get("deaths"),
            "spm": self.data.get("spm") or self.data.get("scorePerMinute"),
        }
        k = self.data.get("kills") or 0
        d = self.data.get("deaths") or 0
        try:
            if d and isinstance(k, (int, float)) and isinstance(d, (int, float)):
                snapshot["kd"] = round(k / d, 2)
            else:
                snapshot["kd"] = "-"
        except Exception:
            snapshot["kd"] = "-"
        self.page_history.add_entry(snapshot)

        user = self.data.get("userName", None)
        platform = self.data.get("platform", None)
        if user and platform:
            self.page_favorites.set_current_player(user, platform)
