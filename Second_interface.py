import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QDrag, QFont, QMouseEvent
from PyQt6.QtCore import Qt, QMimeData, QTimer
from martypy import Marty, MartyConnectException

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

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
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

    def perform_action(self, marty):
        print(f"Performing action for {self.text()}")
        if self.text() == "avancer":
            marty.walk(num_steps=2)
        elif self.text() == "reculer":
            marty.walk(num_steps=2, step_length=-25)
        elif self.text() == "circle_dance":
            marty.circle_dance()
        elif self.text() == "celebrate":
            marty.celebrate();


    def reset_position(self):
        self.setParent(self.original_parent)
        self.move(self.original_position)
        self.show()
        self.dragged = False

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
            button_text = event.mimeData().text()
            existing_button = next((b for b in self.buttons if b.text() == button_text), None)
            if existing_button:
                existing_button.move(event.position().toPoint())
            else:
                button = DraggableButton(button_text, self)
                button.move(event.position().toPoint())
                button.show()
                button.dragged = True
                self.buttons.append(button)
            event.acceptProposedAction()

    def mousePressEvent(self, event):
        for button in self.buttons:
            if button.geometry().contains(event.pos()):
                button.raise_()

    def execute_actions(self):
        try:
            marty = Marty("wifi", "192.168.0.100", blocking=True)  # replace with the appropriate address for your Marty
        except MartyConnectException as e:
            print(f"Failed to connect to Marty: {e}")
            return

        # Sort the buttons by their y-coordinate in ascending order (from top to bottom)
        self.buttons.sort(key=lambda button: button.y())

        def perform_next_action(index):
            if index < len(self.buttons):
                self.buttons[index].perform_action(marty)
                QTimer.singleShot(1000, lambda: perform_next_action(index + 1))

        perform_next_action(0)

    def reset(self):
        while self.buttons:
            button = self.buttons.pop()
            button.reset_position()

# Create the application
app = QApplication(sys.argv)

# Create the main window
window = QWidget()
window.setWindowTitle("Interface Graphique avec Drag-and-Drop")
window.setGeometry(100, 100, 800, 600)
window.setStyleSheet("background-color: #2c3e50;")

# Create the main horizontal layout
main_layout = QHBoxLayout(window)

# Create a vertical layout for the buttons
button_layout = QVBoxLayout()

# Create 5 buttons with specified names and add them to the button layout
button_names = ["avancer", "reculer", "circle_dance", "celebrate"]
buttons = []
for name in button_names:
    button = DraggableButton(name)
    buttons.append(button)
    button_layout.addWidget(button)

# Add the button layout to the main layout
main_layout.addLayout(button_layout)

# Create the main drop area to receive the buttons
drop_area = DropArea()
main_layout.addWidget(drop_area)

# Create the Run button and add it to the main layout
run_button = QPushButton("Run")
run_button.setFont(QFont("Arial", 14))
run_button.setStyleSheet("""
    QPushButton {
        background-color: #27ae60;
        color: white;
        border: 2px solid #1e8449;
        padding: 10px;
    }
    QPushButton:hover {
        background-color: #1e8449;
    }
    QPushButton:pressed {
        background-color: #27ae60;
        border: 2px solid #27ae60;
    }
""")
run_button.clicked.connect(drop_area.execute_actions)
main_layout.addWidget(run_button)

# Create the Reset button and add it to the main layout
reset_button = QPushButton("Reset")
reset_button.setFont(QFont("Arial", 14))
reset_button.setStyleSheet("""
    QPushButton {
        background-color: #c0392b;
        color: white;
        border: 2px solid #e74c3c;
        padding: 10px;
    }
    QPushButton:hover {
        background-color: #e74c3c;
    }
    QPushButton:pressed {
        background-color: #c0392b;
        border: 2px solid #c0392b;
    }
""")
reset_button.clicked.connect(drop_area.reset)
main_layout.addWidget(reset_button)

# Set the main layout for the window
window.setLayout(main_layout)

# Show the window
window.show()

# Execute the application
sys.exit(app.exec())