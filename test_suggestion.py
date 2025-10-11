from PyQt6.QtWidgets import QApplication, QLineEdit, QCompleter, QVBoxLayout, QWidget
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Entry Suggestions")
        
        layout = QVBoxLayout()
        
        # Prepare the suggestion list
        suggestions = ["Apple", "Alps", "Berry", "Cherry", "Banana", "Blueberry", "Apricot"]
        
        # Create a QCompleter
        completer = QCompleter(suggestions)
        
        # Create a QLineEdit
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Start typing for suggestions...")
        
        # Set the completer for the QLineEdit
        self.line_edit.setCompleter(completer)
        
        layout.addWidget(self.line_edit)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())