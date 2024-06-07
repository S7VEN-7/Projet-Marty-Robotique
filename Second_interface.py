import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtGui import QFont
from draggable_button import DraggableButton
from drop_area import DropArea
from styles import BUTTON_STYLE_ACTION

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Interface Graphique avec Drag-and-Drop")
window.setGeometry(100, 100, 800, 600)
window.setStyleSheet("background-color: #2c3e50;")

main_layout = QHBoxLayout(window)

button_layout = QVBoxLayout()

button_names = ["avancer", "reculer", "tourner a droite", "tourner a gauche", "demi_droite", "demi_gauche"]
buttons = []
for name in button_names:
    button = DraggableButton(name)
    buttons.append(button)
    button.setStyleSheet(BUTTON_STYLE_ACTION)
    button_layout.addWidget(button)

main_layout.addLayout(button_layout)

drop_area = DropArea()
main_layout.addWidget(drop_area)


run_button = QPushButton("Run")
run_button.setFont(QFont("Arial", 14))
run_button.setStyleSheet(BUTTON_STYLE_ACTION)
run_button.clicked.connect(drop_area.execute_actions)
main_layout.addWidget(run_button)



reset_button = QPushButton("Reset")
reset_button.setFont(QFont("Arial", 14))
reset_button.setStyleSheet(BUTTON_STYLE_ACTION)
reset_button.clicked.connect(drop_area.reset)
main_layout.addWidget(reset_button)



window.setLayout(main_layout)


window.show()


sys.exit(app.exec())
