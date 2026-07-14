# app/view/SelectionWindow.py
import sys
from pathlib import Path
from PyQt6 import QtWidgets, uic
# ajoute la racine du projet au PYTHONPATH
ROOT = Path(__file__).resolve().parents[3]  # remonte depuis app/classes/view/ -> app -> racine
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from Images import ressources_rc

class ReprintWindowController(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        UI_PATH = ROOT / "app" / "classes" / "view" / "Ui_Reprint.ui" 
        uic.loadUi(UI_PATH , self)
        # connecte ici tes signaux propres à la page si besoin
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    s = ReprintWindowController()
    s.show()
    app.exec()