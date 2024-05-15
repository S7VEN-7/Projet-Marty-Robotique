import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtGui import QDrag , QFont
from PyQt6.QtCore import Qt, QMimeData, QPoint

class DraggableButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Arial", 12))
        self.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: 2px solid #c0392b;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #e74c3c;
                border: 2px solid #e74c3c;
            }
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.text())
        drag.setMimeData(mime_data)
        drag.setHotSpot(event.pos() - self.rect().topLeft())

        drop_action = drag.exec(Qt.DropAction.MoveAction)

class DropArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: #34495e;")
        self.setMinimumSize(400, 400)
        self.buttons = []

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            button = DraggableButton(event.mimeData().text(), self)
            button.move(event.position().toPoint())
            button.show()
            self.buttons.append(button)
            event.acceptProposedAction()

    def mousePressEvent(self, event):
        for button in self.buttons:
            if button.geometry().contains(event.pos()):
                button.raise_()

# Créer l'application
app = QApplication(sys.argv)

# Créer la fenêtre principale
window = QWidget()
window.setWindowTitle("Interface Graphique avec Drag-and-Drop")
window.setGeometry(100, 100, 800, 600)
window.setStyleSheet("background-color: #2c3e50;")

# Créer le layout principal horizontal
main_layout = QHBoxLayout(window)

# Créer un layout vertical pour les boutons
button_layout = QVBoxLayout()

# Créer 10 boutons et les ajouter au layout des boutons
for i in range(10):
    button = DraggableButton(f"Bouton {i + 1}")
    button_layout.addWidget(button)

# Ajouter le layout des boutons au layout principal
main_layout.addLayout(button_layout)

# Créer l'aire de dépôt principale pour recevoir les boutons
drop_area = DropArea()
main_layout.addWidget(drop_area)

# Définir le layout principal pour la fenêtre
window.setLayout(main_layout)

# Afficher la fenêtre
window.show()

# Exécuter l'application
sys.exit(app.exec())
