import subprocess
import sys
import os

# Liste des paquets nécessaires
packages = ["reportlab", "pandas", "numpy"]

for package in packages:
    try:
        __import__(package)
        print("instalation déja faite")
    except ImportError:
        print(f"Installation de '{package}'...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
print("Installation terminé, vous etes prets à utiliser le programme.")
os.system("pause")