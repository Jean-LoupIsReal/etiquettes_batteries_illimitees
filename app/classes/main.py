import subprocess
import sys
import os


# Liste des paquets nécessaires
packages = ["reportlab", "pandas", "numpy", "openpyxl", "pyqt6"]

# Installation des packages non installé sur l'ordinateur
for package in packages:
    try:
        __import__(package)
        #print("instalation déja faite")
    except ImportError:
        #print(f"Installation de '{package}'...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print("Instalation terminé, vous etes prets à utiliser le programme.")
import pandas as pd
from datetime import datetime, date
import traceback
#from model.GenerateurEtiquettes import GenerateurEtiquettes
#from model.EtiquettesFromFile import EtiquettesFromFile
import sys
from PyQt6.QtWidgets import QApplication
from view import ExcelDataView, Ui_MainWindow, Ui_SelectionWindow
from model import DataStore
from controller import ExcelDataController, MainWindowController, SelectionController,DataWindowController, ReprintWindowController, UpdateWindowController


def main() -> int:
    app = QApplication(sys.argv)
    selectionC = SelectionController()
    reprintC = ReprintWindowController()
    updateC = UpdateWindowController()
    dataC = DataWindowController()

    MainMenu_Controller = MainWindowController(selectionC, reprintC, updateC, dataC)


    #data_view = ExcelDataView()
    #data_store = DataStore()
    #controller = ExcelDataController(data_view, data_store)  # noqa: F841 (utilisé via connexions)

    #data_view.show()
    MainMenu_Controller.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

# Loop principal du programme
def main_loop():
    exit_condition = False
    
    while not exit_condition :
        print("===========================================\n" \
            "Que voulez vous faire comme opération?\n" \
            "1 : Imprimer une liste excel d'étiquette\n" \
            "2 : Mettre à jours la liste d'items\n" \
            "3 : test\n" \
            "exit ou q = sortir")
        user_input = input("Reponse : ")
        user_input = user_input.lower()
        match user_input :
            case "1":
                print("recherche fichier excel")
                #e = EtiquettesFromFile()
                #e.creer_pdf()
            case "2":
                print("Mise a jours d'étiquette avec nouveau fichier csv")
            case "3":
                print("3")
            case "exit":  # Default case
                exit_condition = True
                print("exit")
            case "q":  # Default case
                exit_condition = True
                print("exit")
            case _:
                print("mauvais input")
        input("Press Enter to continue...")  # Waits specifically for the spacebar to be pressed
