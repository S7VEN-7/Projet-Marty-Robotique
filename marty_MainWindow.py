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
        self.myMarty1 = Marty("wifi", "192.168.0.106")
        
        user_input = input("Voulez-vous connecter un deuxième Marty ? (Oui/Non) : ")
        while user_input != "Oui" and user_input != "Non":
            user_input = input("Voulez-vous connecter un deuxième Marty ? (Oui/Non) : ")

        if input == "Oui":
            self.two_marty = True
            self.myMarty2 = Marty("wifi", "192.168.0.104")
        else :
            self.myMarty2 = Marty()

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
        self.myMarty1.walk(2, 'auto', 0)
        if self.two_marty != True :
            self.myMarty2.walk(2, 'auto', 0)

    def reculer(self):
        self.myMarty1.walk(2, 'auto', 0, -25)
        if self.two_marty != True :
            self.myMarty2.walk(2, 'auto', 0, -25)

    def droite(self):
        self.myMarty1.sidestep("right", 2)
        if self.two_marty != True :
            self.myMarty2.sidestep("right", 2)

    def gauche(self):
        self.myMarty1.sidestep("left", 2)
        if self.two_marty != True :
            self.myMarty2.sidestep("left", 2)

    def demi_droite(self):
        self.myMarty1.walk(4, 'auto', -13, 30, 2000)
        if self.two_marty != True :
            self.myMarty2.walk(4, 'auto', -13, 30, 2000)
    
    def demi_gauche(self):
        self.myMarty1.walk(4, 'auto', 13, 30, 2000)
        if self.two_marty != True :
            self.myMarty2.walk(4, 'auto', 13, 30, 2000)
    

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
