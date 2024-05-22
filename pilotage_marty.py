import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from martypy import Marty

class MartyControlWidget(QWidget):
    def __init__(self, marty):
        super().__init__()

        self.marty =marty

        self.setWindowTitle("Contrôle de Marty")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.forward_button = QPushButton("Avancer")
        self.forward_button.clicked.connect(self.move_forward)
        layout.addWidget(self.forward_button)

        self.backward_button = QPushButton("Reculer")
        self.backward_button.clicked.connect(self.move_backward)
        layout.addWidget(self.backward_button)

        self.left_button = QPushButton("Tourner à gauche")
        self.left_button.clicked.connect(self.turn_left)
        layout.addWidget(self.left_button)

        self.right_button = QPushButton("Tourner à droite")
        self.right_button.clicked.connect(self.turn_right)
        layout.addWidget(self.right_button)

        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Z:
            self.move_forward()
        elif event.key() == Qt.Key_W:
            self.move_backward()
        elif event.key() == Qt.Key_Q:
            self.turn_left()
        elif event.key() == Qt.Key_D:
            self.turn_right()

    def move_forward(self):
        self.marty.walk(2, 'auto', 0)

    def move_backward(self):
        self.marty.walk(2, 'auto', 90)

    def turn_left(self):
        self.marty.turn_left()

    def turn_right(self):
        self.marty.turn_right()


class MartyController(QMainWindow):
    def __init__(self, marty):
        super().__init__()

        self.marty = marty

        self.setWindowTitle("Contrôleur Marty")
        self.setGeometry(100, 100, 300, 200)

        self.central_widget = MartyControlWidget(self.marty)
        self.setCentralWidget(self.central_widget)


if __name__ == "__main__":
    marty =Marty("wifi","192.168.0.101")

    if marty is None:
        print("Erreur: Marty n'est pas connecté")
        sys.exit(1)

    app = QApplication(sys.argv)
    controller = MartyController(marty)
    controller.show()
    sys.exit(app.exec())
