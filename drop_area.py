from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QMimeData, QTimer
from draggable_button import DraggableButton
from marty_controller import get_marty, perform_action
from styles import DROP_AREA_STYLE, COMMON_BUTTON_STYLE

class DropArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setStyleSheet(DROP_AREA_STYLE)
        self.setMinimumSize(400, 400)
        self.buttons = []

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            button_text = event.mimeData().text()
            existing_button = next((b for b in self.buttons if b.text() == button_text), None)
            if existing_button:
                existing_button.move(event.position().toPoint())
            else:
                button = DraggableButton(button_text, self)
                button.move(event.position().toPoint())
                button.show()
                button.dragged = True
                button.setStyleSheet(COMMON_BUTTON_STYLE)  # Set the style to common style
                self.buttons.append(button)
            event.acceptProposedAction()

    def mousePressEvent(self, event):
        for button in self.buttons:
            if button.geometry().contains(event.pos()):
                button.raise_()

    def execute_actions(self):
        marty = get_marty()
        if not marty:
            return

        # Sort the buttons by their y-coordinate in ascending order (from top to bottom)
        self.buttons.sort(key=lambda button: button.y())

        def perform_next_action(index):
            if index < len(self.buttons):
                perform_action(self.buttons[index].text(), marty)
                QTimer.singleShot(1000, lambda: perform_next_action(index + 1))

        perform_next_action(0)

    def reset(self):
        while self.buttons:
            button = self.buttons.pop()
            button.reset_position()
            button.deleteLater()
