import sys
import pygame
import json
import os
from martypy import Marty
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer
marty1_ip = input("IP du premier robot: ")
class JoystickController(QMainWindow):
    def __init__(self):
        super().__init__()

        pygame.init()
        self.running = True
        self.LEFT, self.RIGHT, self.UP, self.DOWN = False, False, False, False

        self.initUI()
        self.initJoystick()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(16)  # 60 FPS
        self.myMarty = Marty("wifi", marty1_ip)

    def initUI(self):
        self.setWindowTitle("Joystick Controller")
        self.setGeometry(100, 100, 400, 300)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def initJoystick(self):
        if pygame.joystick.get_count() == 0:
            print("No joystick connected.")
            self.running = False
            return
        
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        print("Manette connectée !")
        
        with open(os.path.join(os.path.dirname(__file__), './game_controller/ps4_keys.json')) as file:
            button_keys = json.load(file)

        self.joystick_keys = [key for key in button_keys]

        self.analog_keys = {0: 0, 1: 0, 2: 0, 3: 0, 4: -1, 5: -1}

    def game_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.close()

            self.handle_button_presses(event)
            self.handle_analog_inputs(event)

    def handle_button_presses(self, event):
        if event.type == pygame.JOYBUTTONDOWN:
            button_name = self.joystick_keys[event.button]
            self.log_message(button_name)
            if button_name == "down_arrow":
                self.joystick_rumble(0.65, 1, 250)
                self.reculer()
            elif button_name == "right_arrow":
                self.joystick_rumble(0, 1, 250)
                self.droite()
            elif button_name == "up_arrow":
                self.joystick_rumble(0.65, 1, 250)
                self.avancer()
            elif button_name == "left_arrow":
                self.joystick_rumble(0.65, 0, 250)
                self.gauche()
            elif button_name == "circle":
                self.joystick_rumble(0.65, 1, 250)
                self.demi_droite()
            elif button_name == "square":
                self.joystick_rumble(0.65, 1, 250)
                self.demi_gauche()
            elif button_name == "touchpad":
                self.danse()
            elif button_name == "options":
                self.myMarty.celebrate()
            elif button_name == "share":
                self.running = False
                self.close()

    def handle_analog_inputs(self, event):
        if event.type == pygame.JOYAXISMOTION:
            self.analog_keys[event.axis] = event.value
            self.update_movement(event.axis, event.value)

    def update_movement(self, axis, value):
        if axis in [0, 2]:  # Horizontal
            direction = "LEFT" if value < -0.2 else "RIGHT" if value > 0.2 else None
        elif axis in [1, 3]:  # Vertical
            direction = "UP" if value < -0.2 else "DOWN" if value > 0.2 else None
        else:
            direction = None

        if direction:
            self.log_message(f"{value} {direction}")

        if axis == 4 and value == 1:
            self.log_message("LEFT TRIGGER")
        if axis == 5 and value == 1:
            self.log_message("RIGHT TRIGGER")


    def avancer(self):
        self.myMarty.walk(2, 'auto', 0)

    def reculer(self):
        self.myMarty.walk(2, 'auto', 0, -25)

    def droite(self):
        self.myMarty.sidestep("right", 2)

    def gauche(self):
        self.myMarty.sidestep("left", 2)

    def demi_droite(self):
        self.myMarty.walk(4, 'auto', -13, 30, 2000)
    
    def demi_gauche(self):
        self.myMarty.walk(4, 'auto', 13, 30, 2000)

    def danse(self):
        self.myMarty.dance("right", 3000)

    def joystick_rumble(self, low, high, duration):
        self.joystick.rumble(low, high, duration)

    def log_message(self, message):
        self.text_edit.append(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = JoystickController()
    controller.show()
    sys.exit(app.exec())