import tkinter as tk
from tkinter import filedialog

def choisir_fichier_csv():
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
    
def choisir_fichier_excel():
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