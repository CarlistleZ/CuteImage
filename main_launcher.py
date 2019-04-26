#!/usr/bin/python
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen
import time

from MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    for i in range(5):
        splash = QSplashScreen()
        splash.setPixmap(QPixmap('./Icons/loading_' + str(i) + '.png'))
        splash.show()
        time.sleep(0.3)
        splash.hide()
    window = MainWindow()
    window.show()
    app.exec_()