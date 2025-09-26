import sys
import os
from PyQt6.QtWidgets import QApplication, QFileDialog, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt
import pandas as pd

class ExcelData(QWidget):
    def __init__(self):
        super().__init__()

    def ask_file(self):
        file_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'donnees_magasin')
        print(f"Chemin par défaut pour ouvrir le fichier: {file_folder}")
        file_path, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier Excel", file_folder, "Fichiers Excel (*.xlsx *.xls *.xlsm *.csv);;Tous les fichiers (*)")
        return file_path

    def show_window(self):
        df = self.load_excel_data()
        self.display_data(df)

    def load_excel_data(self, file_path = None):
        if not file_path:
            file_path = self.ask_file()
        if file_path:
            try:
                df = pd.read_excel(file_path) if not file_path.endswith(".csv") else pd.read_csv(file_path)
                return df
            except Exception as e:
                print(f"Erreur lors de la lecture du fichier Excel: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExcelData()
    window.show()
    sys.exit(app.exec())