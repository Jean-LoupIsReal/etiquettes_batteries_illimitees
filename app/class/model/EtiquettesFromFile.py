import subprocess
import sys
import os
import tkinter as tk
from tkinter import filedialog

# Liste des paquets nécessaires
packages = ["reportlab", "pandas", "numpy", "openpyxl"]

# Installation des packages non installé sur l'ordinateur
for package in packages:
    try:
        __import__(package)
        #print("instalation déja faite")
    except ImportError:
        #print(f"Installation de '{package}'...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print("Instalation terminé, vous etes prets à utiliser le programme.")

print("Selectionnez votre fichier Excel pour les etiquettes.")
import pandas as pd
from datetime import datetime, date
import traceback
from GenerateurEtiquettes import GenerateurEtiquettes

class EtiquettesFromFile:
    # Chemin absolu basé sur le script lui-même
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PATH_DATA_FOLDER = os.path.join(BASE_DIR, "../../", "data/")
    CSV_SERVEX_PATH = os.path.join(PATH_DATA_FOLDER, "/donnees_magasin/", "Servex_nettoye.csv")

    # Crée le PDF avec les informations demandés à l'utilisateur
    def creer_pdf(self): 
        print(self.CSV_SERVEX_PATH)
        # Déclarer les variable des données
        df_inventaire = pd.read_csv(self.CSV_SERVEX_PATH)
        #choisir le fichier à imprimer
        df_impression = pd.read_excel(self.choisir_fichier_excel())
        #location = self.ask_location()
        #Enlève les lignes vides
        df_impression = df_impression[df_impression.iloc[:, 0].notna()].reset_index(drop=True)
        df_impression["No"] = df_impression.iloc[:,0]
        df_impression = df_impression.merge(df_inventaire, on="No", how="left")
        
        # Cree le pdf avec le nom etiquettes + la date du 
        current_datetime = datetime.now()
        now = current_datetime.strftime("%Y-%m-%d-%H-%M")
        generateur_etiquettes = GenerateurEtiquettes()
        
        data_etiquettes = df_impression.groupby(["No"]).first()
        emplacement_fichier = os.path.join(self.PATH_DATA_FOLDER, f"etiquettes-{now}.pdf")
        generateur_etiquettes.generer_pdf_etiquettes(data_etiquettes, emplacement_fichier)

    def choisir_fichier_csv(self):
        # Création de la fenêtre (invisible)
        root = tk.Tk()
        root.withdraw()

        # Ouvre l'explorateur de fichiers
        fichier_csv = filedialog.askopenfilename(
            title="Choisissez un fichier CSV",
            filetypes=[("Fichiers CSV", "*.csv")]
        )
        if fichier_csv:
            print(f"Fichier sélectionné : {fichier_csv}")
            return fichier_csv
        else:
            print("Aucun fichier sélectionné.")
            return None
        
    def choisir_fichier_excel(self):
        # Création de la fenêtre (invisible)
        root = tk.Tk()
        root.withdraw()

        # Ouvre l'explorateur de fichiers
        fichier_xlsm = filedialog.askopenfilename(
            title="Choisissez un fichier CSV",
            filetypes=[("Fichiers XLSM", "*.xlsm")]
        )

        if fichier_xlsm:
            print(f"Fichier sélectionné : {fichier_xlsm}")
            return fichier_xlsm
        else:
            print("Aucun fichier sélectionné.")
            return None
 
# Execution du script
if __name__ == "__main__":
    e = EtiquettesFromFile()
    try:
        e.creer_pdf()
    except Exception as e:
        print("Une erreur est survenue :")
        traceback.print_exc()
        os.system("pause")  # Attends que l'utilisateur appuie sur u ne touche
    