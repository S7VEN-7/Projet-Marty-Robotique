from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import *
from ui_MainWindow import Ui_MainWindow
from marty_MainWindow import MartyMainWindow
app = QApplication(sys.argv)
window = MartyMainWindow()
window.show()
rc = app.exec()
sys.exit(rc)