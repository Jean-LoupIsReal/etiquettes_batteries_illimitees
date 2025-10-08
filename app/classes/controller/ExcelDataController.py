import sys
import os
from PyQt6.QtWidgets import QApplication, QFileDialog, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt
import pandas as pd
from view import ExcelDataView, ErrorView
from model import DataStore

class ExcelDataController():
    
    def __init__(self, view: ExcelDataView, model: DataStore) -> None:
        self.view = view
        self.model = model
        # Connexions
        self.view.open_file_requested.connect(self.on_open_file)
    
    def on_open_file(self) -> None:
        try:
            file_name = self.model.ask_file(self.view)
            df = self.model.load_excel_data(file_name)
        except Exception as e:
            ev = ErrorView()
            ev.display_error(f"Erreur lors de la lecture du fichier Excel : {e}")
            return
        if isinstance(df, pd.DataFrame):
            self.view.display_data(df)
        else:
            ev = ErrorView()
            ev.display_error(f"Votre fichier est corrompu, le programme n'est pas capable de le lire")
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tester = ExcelDataController()
    tester