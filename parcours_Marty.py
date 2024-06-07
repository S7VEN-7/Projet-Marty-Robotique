from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QColor
from martypy import Marty

class Marty:
    def __init__(self, name, ip_address=None):
        self.name = name
        self.ip_address = ip_address
        if self.ip_address:
            self.connect_to_marty()

    def connect_to_marty(self):
        self.marty = Marty(self.ip_address)
        print(f"Connected to {self.name} at {self.ip_address}")

    def move_to(self, position):
        print(f"{self.name} moving to {position}")
        # Translate the position into a movement command for the Marty robot
        if hasattr(self, 'marty'):
            self.marty.move_to(position)  # Command to move Marty to a specific position

    def recognize_color(self, color):
        print(f"{self.name} recognizes color {color.name()}")
        # Any specific behavior for recognizing colors can be added here

class MartyControlWidget(QWidget):
    def __init__(self, marty1, marty2):
        super().__init__()
        self.marty1 = marty1
        self.marty2 = marty2
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.move_button = QPushButton("Start Moving")
        self.move_button.clicked.connect(self.start_movement)
        layout.addWidget(self.move_button)
        self.setLayout(layout)

    def start_movement(self):
        # Define the 3x3 grid with colors
        grid = [[QColor("blue"), QColor("green"), QColor("green")],
                [QColor("yellow"), QColor("cyan"), QColor("red")],
                [QColor("yellow"), QColor("yellow"), QColor("pink")]]
        
        # Find the start and end positions
        start = self.find_position(grid, QColor("blue"))
        end = self.find_position(grid, QColor("red"))

        if start and end:
            path = self.calculate_path(grid, start, end)
            for position in path:
                self.marty1.move_to(position)
                self.marty2.move_to(position)
                self.marty1.recognize_color(grid[position[0]][position[1]])
                self.marty2.recognize_color(grid[position[0]][position[1]])

    def find_position(self, grid, color):
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == color:
                    return (row, col)
        return None

    def calculate_path(self, grid, start, end):
        path = [start]
        current_position = start

        while current_position != end:
            row, col = current_position
            current_color = grid[row][col]
            
            if current_color == QColor("green"):  # Move up
                if row > 0:
                    next_position = (row - 1, col)
            elif current_color == QColor("yellow"):  # Move left
                if col > 0:
                    next_position = (row, col - 1)
            elif current_color == QColor("magenta"):  # Move right
                if col < len(grid[row]) - 1:
                    next_position = (row, col + 1)
            elif current_color == QColor("pink"):  # Move down
                if row < len(grid) - 1:
                    next_position = (row + 1, col)
            else:
                break
            
            if next_position == current_position or next_position in path:
                break

            current_position = next_position
            path.append(current_position)

        return path

class MartyController(QMainWindow):
    def __init__(self, marty1, marty2):
        super().__init__()

        self.marty1 = marty1
        self.marty2 = marty2

        self.setWindowTitle("Contrôleur Marty")
        self.setGeometry(100, 100, 300, 200)

        self.central_widget = MartyControlWidget(self.marty1, self.marty2)
        self.setCentralWidget(self.central_widget)

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    marty1 = Marty("Marty1", "192.168.0.106")
    marty2 = Marty("Marty2")
    controller = MartyController(marty1, marty2)
    controller.show()
    sys.exit(app.exec_())
