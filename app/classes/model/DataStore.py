import sys
import os
from PyQt6.QtWidgets import QApplication, QFileDialog
import pandas as pd

"""
Model: responsable du chargement et de la préparation des données.
"""
class DataStore:
    def ask_file(self, widget):
        file_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'donnees_magasin')
        print(f"Chemin par défaut pour ouvrir le fichier: {file_folder}")
        file_path, _ = QFileDialog.getOpenFileName(widget, "Ouvrir un fichier Excel", file_folder, "Fichiers Excel (*.xlsx *.xls *.xlsm *.csv);;Tous les fichiers (*)")
        return file_path
    
    """
    Charge un CSV ou un Excel dans un DataFrame Pandas.
    """
    def load_excel_data(self, file_path = None):
        if file_path:
            try:
                df = pd.read_excel(file_path) if not file_path.endswith(".csv") else pd.read_csv(file_path)
                return df
            except Exception as e:
                print(f"Erreur lors de la lecture du fichier Excel: {e}")