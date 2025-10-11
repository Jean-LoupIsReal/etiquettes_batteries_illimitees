import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow
from . import SelectionController, DataWindowController, ReprintWindowController, UpdateWindowController
# ajoute la racine du projet au PYTHONPATH
ROOT = Path(__file__).resolve().parents[3]  # remonte depuis app/view/ -> app -> racine
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from app.classes.view import Ui_MainWindow
from Images import ressources_rc  # ou: import ressources_rc si tu l’as déplacé
#from view import Ui_MainWindow, Ui_SelectionWindow
class MainWindowController(QMainWindow):
    def __init__(self, selectionC: SelectionController, reprintC: ReprintWindowController, updateC: UpdateWindowController, dataC: DataWindowController,parent=None): # ajouter , HomeWindowC : HomeWindowController, ReprintC : ReprintWindowController, UpdateWindowC : UpdateWindowController, DataWindowC, DatWindowaController
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Vous pouvez maintenant accéder aux widgets via self.ui.nom_du_widget
        
        self.ui.body.addWidget(selectionC)
        self.ui.body.addWidget(dataC)
        self.ui.body.addWidget(reprintC)
        self.ui.body.addWidget(updateC)
        # Connection des boutons
        
        self.ui.body.setCurrentIndex(0)
        # Home page
        self.ui.home_btn.clicked.connect(lambda: self.ui.body.setCurrentWidget(self.ui.home_widget))
        # Selection page
        self.ui.selection_btn.clicked.connect(lambda: self.ui.body.setCurrentWidget(selectionC))
        # Reprint page
        self.ui.reprint_btn.clicked.connect(lambda: self.ui.body.setCurrentWidget(reprintC))
        # Update page
        self.ui.update_btn.clicked.connect(lambda : self.ui.body.setCurrentWidget(updateC))
        # Data page
        self.ui.data_btn.clicked.connect(lambda : self.ui.body.setCurrentWidget(dataC))


    
    def change_widget():
        pass
