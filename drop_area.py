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
        self.button_counters = {}

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            button_text = event.mimeData().text()

            for button in self.buttons:
                if button.text() == button_text:
                    button.move(event.position().toPoint())
                    button.show()
                    event.acceptProposedAction()
                    return

            if button_text in self.button_counters:
                self.button_counters[button_text] += 1
            else:
                self.button_counters[button_text] = 1

            unique_button_text = f"{button_text}{self.button_counters[button_text]}"
            button = DraggableButton(unique_button_text, self)
            button.move(event.position().toPoint())
            button.show()
            button.dragged = True
            button.setStyleSheet(COMMON_BUTTON_STYLE)
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

        self.buttons.sort(key=lambda button: button.y())

        def perform_next_action(index):
            if index < len(self.buttons):
                base_action_name = ''.join(filter(lambda x: x.isalpha() or x == ' ' or x == '_', self.buttons[index].text())).strip()
                perform_action(base_action_name, marty)
                QTimer.singleShot(1000, lambda: perform_next_action(index + 1))

        perform_next_action(0)

    def reset(self):
        while self.buttons:
            button = self.buttons.pop()
            button.reset_position()
            button.deleteLater()
        self.button_counters.clear()
