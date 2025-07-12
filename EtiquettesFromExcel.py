import subprocess
import sys
import os

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
from choisir_fichier import choisir_fichier_excel
from GenerateurEtiquettes import GenerateurEtiquettes

class EtiquettesFromExcel:
    # Chemin absolu basé sur le script lui-même
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CSV_SERVEX_PATH = os.path.join(BASE_DIR, "FichierDonnees", "Servex_nettoye.csv")

    # Crée le PDF avec les informations demandés à l'utilisateur
    def creer_pdf(self): 
        # Déclarer les variable des données
        df_inventaire = pd.read_csv(self.CSV_SERVEX_PATH)
        #choisir le fichier à imprimer
        df_impression = pd.read_excel(choisir_fichier_excel())

        #location = self.ask_location()
        #Enlève les lignes vides
        df_impression = df_impression[df_impression.iloc[:, 0].notna()].reset_index(drop=True)
        df_impression["No"] = df_impression.iloc[:,0]

        df_impression = df_impression.merge(df_inventaire, on="No", how="left")
        #df_impression["No"] = df_impression([])

        # Cree le pdf avec le nom etiquettes + la date du 
        current_datetime = datetime.now()
        now = current_datetime.strftime("%Y-%m-%d-%H-%M")
        generateur_etiquettes = GenerateurEtiquettes()
        generateur_etiquettes.generer_pdf_etiquettes(df_impression.groupby(["No"]).first(), os.path.join(self.BASE_DIR, f"etiquettes-{now}.pdf"), False)

 
# Execution du script
if __name__ == "__main__":
    e = EtiquettesFromExcel()
    try:
        e.creer_pdf()
    except Exception as e:
        print("Une erreur est survenue :")
        traceback.print_exc()
        os.system("pause")  # Attends que l'utilisateur appuie sur u ne touche
    