import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from PyQt6.QtWidgets import QApplication, QMainWindow

from K22416C.FINAL.UI.loginmyfilmExt import loginmyfilmExt

app=QApplication([])
mainwindow=QMainWindow()
myui=loginmyfilmExt()
myui.setupUi(mainwindow)
myui.showWindow()
app.exec()

