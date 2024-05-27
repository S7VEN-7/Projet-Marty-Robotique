import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtGui import QFont
from draggable_button import DraggableButton
from drop_area import DropArea
from styles import BUTTON_STYLE_ACTION

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
button_names = ["avancer", "reculer", "circle_dance", "eyes", "piww", "arms"]
buttons = []
for name in button_names:
    button = DraggableButton(name)
    buttons.append(button)
    button.setStyleSheet(BUTTON_STYLE_ACTION)  # Apply common style to all buttons
    button_layout.addWidget(button)
# Add the button layout to the main layout
main_layout.addLayout(button_layout)

# Create the main drop area to receive the buttons
drop_area = DropArea()
main_layout.addWidget(drop_area)

# Create the Run button and add it to the main layout
run_button = QPushButton("Run")
run_button.setFont(QFont("Arial", 14))
run_button.setStyleSheet(BUTTON_STYLE_ACTION)  # Apply the new style here
run_button.clicked.connect(drop_area.execute_actions)
main_layout.addWidget(run_button)

# Create the Reset button and add it to the main layout
reset_button = QPushButton("Reset")
reset_button.setFont(QFont("Arial", 14))
reset_button.setStyleSheet(BUTTON_STYLE_ACTION)  # Apply the new style here
reset_button.clicked.connect(drop_area.reset)
main_layout.addWidget(reset_button)

# Set the main layout for the window
window.setLayout(main_layout)

# Show the window
window.show()

# Execute the application
sys.exit(app.exec())
