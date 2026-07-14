# app/view/SelectionWindow.py
import sys
from pathlib import Path
from PyQt6 import QtWidgets, uic
# ajoute la racine du projet au PYTHONPATH
ROOT = Path(__file__).resolve().parents[3]  # remonte depuis app/classes/view/ -> app -> racine
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from Images import ressources_rc
from app.classes.model import DataStore, EtiquettesFromFile

class DataWindowController(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        UI_PATH = ROOT / "app" / "classes" / "view" / "Ui_Data.ui" 
        uic.loadUi(UI_PATH , self)#<-- applique l'UI sur CE widget
        # connecte ici tes signaux propres à la page si besoin
        self.select_file_btn
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    s = DataWindowController()
    s.show()
    app.exec()