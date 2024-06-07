from PyQt6.QtWidgets import QPushButton, QApplication
from PyQt6.QtGui import QFont, QMouseEvent, QDrag
from PyQt6.QtCore import Qt, QMimeData

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
        self.dragged = False
        self.original_parent = parent
        self.original_position = self.pos()

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

    def reset_position(self):
        self.setParent(self.original_parent)
        self.move(self.original_position)
        self.show()
        self.dragged = False
