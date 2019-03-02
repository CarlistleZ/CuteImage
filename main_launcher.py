#!/usr/bin/python
from PyQt5.QtWidgets import QApplication
import sys, platform

from MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()

    window.show()
    app.exec_()