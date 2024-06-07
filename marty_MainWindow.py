#marty_MainWindow.py
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QWidget
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QKeyEvent
from martypy import Marty
from ui_MainWindow import Ui_MainWindow

import joystick

class MartyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MartyMainWindow,self).__init__(parent)
        self.setupUi(self)

        self.two_marty = False
        self.martyRobots = []

        self.myMarty1 = Marty("wifi", "192.168.0.106")
        self.martyRobots.append(self.myMarty1)
        
        user_input = input("Voulez-vous connecter un deuxième Marty ? (Oui/Non) : ")
        while user_input != "Oui" and user_input != "Non":
            user_input = input("Voulez-vous connecter un deuxième Marty ? (Oui/Non) : ")

        if input == "Oui":
            self.two_marty = True
            self.myMarty2 = Marty("wifi", "192.168.0.104")
            self.martyRobots.append(self.myMarty2)


        self.up.clicked.connect(self.avancer)
        self.down.clicked.connect(self.reculer)
        self.right.clicked.connect(self.droite)
        self.left.clicked.connect(self.gauche)
        self.rotate_right.clicked.connect(self.demi_droite)
        self.rotate_left.clicked.connect(self.demi_gauche)

        self.controller = joystick.JoystickController()
        self.controller.game_loop()

    @pyqtSlot()
    def on_actionQuitter_triggered(self):
        self.close()
        
    def closeEvent(self,event):
        messageConfirmation = "Êtes-vous sûr de vouloir quitter MartyApp ?"
        reponse = QMessageBox.question(self,"Confirmation",
                          messageConfirmation,QMessageBox.StandardButton.Yes,QMessageBox.StandardButton.No)
        if reponse == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

    def avancer(self):
        for marty in self.martyRobots:
            marty.walk(2, 'auto', 0)

    def reculer(self):
        for marty in self.martyRobots:
            marty.walk(2, 'auto', 0, -25)

    def droite(self):
        for marty in self.martyRobots:
            marty.sidestep("right", 2)

    def gauche(self):
        for marty in self.martyRobots:
            marty.sidestep("left", 2)

    def demi_droite(self):
        for marty in self.martyRobots:
            marty.walk(4, 'auto', -13, 30, 2000)
    
    def demi_gauche(self):
        for marty in self.martyRobots:
            marty.walk(4, 'auto', 13, 30, 2000)


    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        if key == Qt.Key.Key_Z:
            self.avancer()
        elif key == Qt.Key.Key_Q:
            self.gauche()
        elif key == Qt.Key.Key_S:
            self.reculer()
        elif key == Qt.Key.Key_D:
            self.droite()
        elif key == Qt.Key.Key_E:
            self.demi_droite()
        elif key == Qt.Key.Key_A:
            self.demi_gauche()
        elif key == Qt.Key.Key_O:
            self.block()
        elif key == Qt.Key.Key_B:
            color = self.myMarty1.get_color_sensor_hex("left")
            if((color > "300000") and (color <= "339999")):
                print("violet")
            if((color > "340000") and (color <= "390000")):
                print("vert")
            if((color > "3a0000") and (color <= "3fffff")):
                print("bleu")
            if((color > "900000") and (color <= "a50000")):
                print("rouge")
            if(color > "ab0000"):
                print("jaune")
    def block(self):
        color = self.myMarty1.get_ground_sensor_reading(add_on_or_side='left')
        print(color)
        self.avancer()
        self.avancer()
        self.avancer()
        color = self.myMarty1.get_ground_sensor_reading(add_on_or_side='left')
        print(color)
        self.avancer()
        self.avancer()
        
    def get_color_sensor_hex(self, add_on_or_side: str) -> str:
        [foot_on_ground, raw_data] = self._get_color_sensor_raw_data(add_on_or_side) # (clear, red, green, blue)
        if len(raw_data) > 0:
            hex_color = self.rgb_to_hex((raw_data[1], raw_data[2], raw_data[3]))
            return hex_color
        return 0