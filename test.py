from PyQt6.QtWidgets import QListWidget, QApplication
from PyQt6.QtCore import Qt

app = QApplication([])
list_widget = QListWidget()
list_widget.addItems(["Item 1", "Item 2", "Item 3"])
list_widget.show()

# To get selected items:
selected_items = list_widget.selectedItems()
for item in selected_items:
    print(item.text())

# To get selected indexes (more versatile for complex models):
selection_model = list_widget.selectionModel()
selected_indexes = selection_model.selectedIndexes()
for index in selected_indexes:
    print(index.data())

app.exec()