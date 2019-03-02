from itertools import product
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMdiSubWindow, QLabel, QMessageBox, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage, qRgb, qRed, qGreen, qBlue

import cclabel
from GrayScaleImageWindow import GrayscaleImageWindow


class RgbImageWindow(QMdiSubWindow):
    def __init__(self, name = "", parent = None):
        QMdiSubWindow.__init__(self)
        self.name = name
        self.parent = parent
        self.initUI()
        self.setAttribute(Qt.WA_DeleteOnClose)

    def initUI(self):
        # ShortName only contains the name, not the path
        self.shortName = self.name.split("/")[-1]
        self.setWindowTitle(self.shortName)


        # Create an image
        self.pixmap = QPixmap()
        self.image_label = QLabel()

        if self.parent == 0:
            # Create a new image from name
            self.image = QImage(self.name)
        else:
            # Create an image from parent with the same dimension
            self.image = QImage(self.parent.image.size(), self.parent.image.format())

        if not self.image.isNull():
            self.loaded_image = True
            self.update_pixmap(self.image)
        else:
            QMessageBox(self, "Error", "Unable to create a new image in a new window.")

        self.setWidget(self.image_label)
        self.resize(self.pixmap.size())
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def update_pixmap(self, image):
        self.pixmap = QPixmap.fromImage(image)
        self.image_label.resize(self.pixmap.size())
        self.image_label.setPixmap(self.pixmap.fromImage(image))
        self.resize(self.pixmap.size())

    def traverse_image(self, method, mode="RGB", with_neighbors=False):
        if self.loaded_image:
            if mode == "grayscale":
                sub_window = GrayscaleImageWindow(self.name, self)
            else:
                sub_window = RgbImageWindow(self.name, self)
            if sub_window:
                for x, y in product(range(self.image.height()), range(self.image.width())):
                    if not with_neighbors:
                        pixel = self.image.pixel(x, y)
                        new_pixel = method(pixel)
                    else:
                        new_pixel = method(self.image, x, y)
                    sub_window.image.setPixel(x, y, new_pixel)
                sub_window.update_pixmap(sub_window.image)
                return sub_window

    def reverse(self):
        def calc_reverse(pixel):
            return qRgb(255 - qRed(pixel), 255 - qGreen(pixel), 255 - qBlue(pixel))
        return self.traverse_image(calc_reverse)

    def saturate_red(self):
        def calc_saturate_red(pixel):
            return qRgb(255, qGreen(pixel), qBlue(pixel))
        return self.traverse_image(calc_saturate_red)

    def saturate_green(self):
        def calc_saturate_green(pixel):
            return qRgb(qRed(pixel), 255, qBlue(pixel))
        return self.traverse_image(calc_saturate_green)

    def saturate_blue(self):
        def calc_saturate_blue(pixel):
            return qRgb(qRed(pixel), qGreen(pixel), 255)
        return self.traverse_image(calc_saturate_blue)

    def to_grayscale(self):
        def calc_to_grayscale(pixel):
            return 0.299 * qRed(pixel) + 0.587 * qGreen(pixel) + 0.114 * qBlue(pixel)
        return self.traverse_image(calc_to_grayscale, "grayscale")

    # todo
    def set_rgb(self):
        print("set_rgb clicked")

    def ccl(self):
        cclabel.ccl(self.name)