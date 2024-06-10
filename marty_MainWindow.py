#marty_MainWindow.py
from PyQt6.QtCore import Qt
import numpy as np
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QWidget
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QKeyEvent
from martypy import Marty
from ui_MainWindow import Ui_MainWindow

import joystick
from joystick import marty1_ip
class MartyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MartyMainWindow,self).__init__(parent)
        self.setupUi(self)

        self.two_marty = False
        self.martyRobots = []
        self.myMarty1 = Marty("wifi", marty1_ip)
        self.martyRobots.append(self.myMarty1)
        
        user_input = input("Voulez-vous connecter un deuxième Marty ? (Oui/Non) : ")
        while user_input != "Oui" and user_input != "Non":
            user_input = input("Voulez-vous connecter un deuxième Marty ? (Oui/Non) : ")

        if user_input == "Oui":
            self.two_marty = True
            marty2_ip = input("IP du deuxème robot: ")
            self.myMarty2 = Marty("wifi", marty2_ip)
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
            marty.walk(6, 'auto', 0)

    def reculer(self):
        for marty in self.martyRobots:
            marty.walk(6, 'auto', 0, -25)

    def droite(self):
        for marty in self.martyRobots:
            marty.sidestep("right", 5)

    def gauche(self):
        for marty in self.martyRobots:
            marty.sidestep("left", 5)

    def demi_droite(self):
        for marty in self.martyRobots:
            marty.walk(4, 'auto', -13, 30, 2000)
    
    def demi_gauche(self):
        for marty in self.martyRobots:
            marty.walk(4, 'auto', 13, 30, 2000)
    position = [1, 2]
    matrice_marty1 = np.array([
    [2, 2, 4],
    [0, 0, 0],
    [5, 5, 0]
    ])
    matrice_marty2 = np.array([
    [0, 0, 0],
    [5, 4, 9],
    [0, 0, 2]
    ])
    
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
        elif key == Qt.Key.Key_P:
            self.check_path(self.matrice_marty1, self.matrice_marty2, self.position)
        elif key == Qt.Key.Key_B:
            color = self.myMarty1.get_color_sensor_hex("left")
            self.hexcolor(color)
    
    def hexcolor(self, color):
        if((color > "300000") and (color <= "339999")):
            return 1
        if((color > "340000") and (color <= "390000")):
            return 2
        if((color > "3a0000") and (color <= "3fffff")):
            return 3
        if((color > "900000") and (color <= "a50000")):
            return 4
        if(color > "ab0000"):
            return 5
    
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
    def check_path(self, matrice_marty1, matrice_marty2, pos):
        tabmouvement = []
        for i in range(matrice_marty1.shape[0]):
            for j in range(matrice_marty1.shape[1]):
                temp1 = matrice_marty1[i][j]
                temp2 = matrice_marty2[i][j]
                if(temp1 == 0):
                    matrice_marty1[i][j] = temp2
                if(temp2 == 0):
                    matrice_marty2[i][j] = temp1
                print(matrice_marty1[i][j], end=" ")
            print()
        deplacementx = pos[0];
        deplacementy = pos[1];
        tab = [0 ,0 ,0 ,0]
        for i in range (4):
            if(i == 0):
                deplacementy -= 1
                if(deplacementy >= 0):
                    tab[i] = 1
                deplacementy += 1
            elif(i == 1):
                    deplacementx += 1
                    if(deplacementx < 3):
                        tab[i] = 1
                    deplacementx -= 1
            elif(i == 2):
                    deplacementy += 1
                    if(deplacementy < 3):
                        tab[i] = 1
                    deplacementy -= 1
            elif(i == 3):
                    deplacementx-= 1
                    if(deplacementx >= 0):
                        tab[i] = 1
                    deplacementx += 1
        premier_mouvement = 0
        print("position",matrice_marty1[pos[1]][pos[0]])
        for i in range(4):
            print("i=", i)
            premier_mouvement = 0
            if(tab[i] == 1):
                tabmouvement = []
                deplacementx = pos[0]
                deplacementy = pos[1]
                for j in range (8):
                    print("j=",j)
                    if(premier_mouvement == 0):
                        if(i == 0):
                            deplacementy -= 1
                            mouv = 5
                        elif(i == 1):
                            deplacementx += 1
                            mouv = 2
                        elif(i == 2):
                            deplacementy += 1
                            mouv = 4
                        elif(i == 3):
                            deplacementx -= 1
                            mouv = 1
                        premier_mouvement = 1
                        tabmouvement.append(mouv)
                    mouv = matrice_marty1[deplacementy][deplacementx]
                    print("mouvement", mouv)
                    if((mouv == 5) and (deplacementy - 1 >= 0)):
                        deplacementy -= 1
                    elif(mouv == 2) and (deplacementx + 1 < 3):
                        deplacementx += 1
                    elif(mouv == 4) and (deplacementy + 1 < 3):
                        deplacementy += 1
                    elif(mouv == 1) and (deplacementx - 1 >= 0):
                        deplacementx -= 1
                    elif(mouv == 9):
                        print(tabmouvement)
                        for mouv in tabmouvement:
                            if(mouv == 1):
                                self.gauche()
                            elif(mouv == 2):
                                self.droite()
                            elif(mouv == 5):
                                self.avancer()
                            elif(mouv == 4):
                                self.reculer()
                        return True
                    print(mouv)
                    tabmouvement.append(mouv)