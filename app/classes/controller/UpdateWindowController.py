# app/view/SelectionWindow.py
import sys
from pathlib import Path
from PyQt6 import QtWidgets
# ajoute la racine du projet au PYTHONPATH
ROOT = Path(__file__).resolve().parents[3]  # remonte depuis app/classes/view/ -> app -> racine
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from app.classes.view import Ui_UpdateWindow  # adapte le chemin
from Images import ressources_rc

class UpdateWindowController(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_UpdateWindow()
        self.ui.setupUi(self)   # <-- applique l'UI sur CE widget
        # connecte ici tes signaux propres à la page si besoin
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    s = UpdateWindowController()
    s.show()
    app.exec()