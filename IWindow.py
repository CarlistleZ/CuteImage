#!/usr/bin/python
from PyQt5.QtWidgets import QMdiArea

from GrayScaleImageWindow import GrayscaleImageWindow
from RgbImageWindow import RgbImageWindow


class IWindow(QMdiArea):
    def __init__(self, parent):
        QMdiArea.__init__(self, parent)
        self.parent = parent;
        self.subWindowActivated.connect(self.update_window)

    def update_window(self):
        active_window = self.activeSubWindow()
        if not active_window:
            return
        self.parent.bwindow.update_image_info(active_window.name)

    def closeWindowHandler(self):
        # TODO
        self.parent.rwindow.indicateClosedWindow("dassadds")
