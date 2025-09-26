import sys

# 1. Import QApplication and all the required widgets
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QTextEdit, QLineEdit, QVBoxLayout
from PyQt6.QtGui import QIcon
class MenuPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu Principal")
        self.setGeometry(100, 100, 300, 200)
        self.setWindowIcon(QIcon('path/to/icon.png'))  # Optional: Set a window icon

        layout = QVBoxLayout()

        self.label = QLabel("Bienvenue dans le programme d'étiquettes")
        layout.addWidget(self.label)

        self.button1 = QPushButton("Imprimer une liste excel d'étiquette")
        self.button1.clicked.connect(self.handle_button1)
        layout.addWidget(self.button1)

        self.button2 = QPushButton("Mettre à jours la liste d'items")
        self.button2.clicked.connect(self.handle_button2)
        layout.addWidget(self.button2)

        self.button3 = QPushButton("Test")
        self.button3.clicked.connect(self.handle_button3)
        layout.addWidget(self.button3)

        self.setLayout(layout)

    def handle_button1(self):
        print("Bouton 1 cliqué - Imprimer une liste excel d'étiquette")

    def handle_button2(self):
        print("Bouton 2 cliqué - Mettre à jours la liste d'items")

    def handle_button3(self):
        print("Bouton 3 cliqué - Test")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MenuPrincipal()
    window.show()
    sys.exit(app.exec())