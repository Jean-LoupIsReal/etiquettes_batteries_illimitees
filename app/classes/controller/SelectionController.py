# app/view/SelectionWindow.py
import sys
import pandas as pd
from pathlib import Path
from PyQt6 import QtWidgets, uic
# ajoute la racine du projet au PYTHONPATH
ROOT = Path(__file__).resolve().parents[3]  # remonte depuis app/classes/view/ -> app -> racine
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from Images import ressources_rc
UI_PATH = ROOT / "app" / "classes" / "view" / "SelectionUI.ui" 
CURRENT_DB_PATH = ROOT / "app" / "data" / "donnees_magasin" / "Servex_nettoye.csv"

class SelectionController(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(UI_PATH , self)
        self.db = pd.read_csv(CURRENT_DB_PATH)
        # connecte ici tes signaux propres à la page si besoin

    def refresh_db(self):
        self.db = pd.read_csv(CURRENT_DB_PATH)


        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    s = SelectionController()
    s.show()
    app.exec()