from PyQt6.QtWidgets import QMessageBox, QWidget

class ErrorView(QWidget):
    def __init__(self):
        super().__init__()
        
    def display_error(self, error):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Erreur")
        msg.setText(error)
        msg.exec()