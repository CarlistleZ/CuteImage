#!/usr/bin/python
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel

# Right window in the main window
class RWindow(QFrame):
    def __init__(self, parent):
        QFrame.__init__(self, parent)
        self.parent = parent;
        self.rootVbox = QVBoxLayout()
        self.lbl = QLabel("r window correct!")
        self.lbl2 = QLabel("_")
        self.rootVbox.addWidget(self.lbl)
        self.setLayout(self.rootVbox)

    def changeLabelText(self, text):
        self.lbl.setText(text)

    def indicateClosedWindow(self, window_name):
        self.lbl2.setText(self.lbl2.text() + "\nYou closed "+window_name+" !")