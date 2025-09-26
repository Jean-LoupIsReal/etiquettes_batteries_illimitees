import sys

# 1. Import QApplication and all the required widgets
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QTextEdit, QLineEdit, QVBoxLayout
from PyQt6.QtGui import QIcon

def MyApp():
    # 2. Create an instance of QApplication
    app = QApplication(sys.argv)

    # 3. Create your application's GUI
    window = QWidget()
    window.setWindowTitle("EtiquApp")
    window.setGeometry(100, 100, 280, 80)
    helloMsg = QLabel("<h1>Hello, World!</h1>", parent=window)
    helloMsg.move(60, 15)

    # 4. Show the window
    window.show() 

    # 5. Start the event loop
    sys.exit(app.exec())

MyApp()
