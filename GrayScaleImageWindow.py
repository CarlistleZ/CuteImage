import math
from itertools import product

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMdiSubWindow, QLabel, QMessageBox, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage, qRgb, qRed, qGreen, qBlue


class GrayscaleImageWindow(QMdiSubWindow):
    MAX_BRIGHTNESS = 255
    COLOR_TABLE_SIZE = 256

    def __init__(self, name="", parent=None):
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
            self.image = QImage(self.parent.image.size(), QImage.Format_Indexed8)
            self.image.setColorCount(GrayscaleImageWindow.COLOR_TABLE_SIZE)
            self.origin_color()

        if not self.image.isNull():
            self.loaded_image = True
            self.update_pixmap(self.image)
        else:
            QMessageBox(self, "Error", "Unable to create a new gray scale image in a new window.")

        self.setWidget(self.image_label)
        self.resize(self.pixmap.size())
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def update_pixmap(self, image):
        self.copy_image(image)
        self.image_label.resize(self.pixmap.size())
        self.image_label.setPixmap(self.pixmap.fromImage(image))
        self.resize(self.pixmap.size())

    def copy_image(self, image):
        self.pixmap = QPixmap.fromImage(image)
        if self.pixmap.isNull():
            QMessageBox.information(self, "Error", "Unable to load pixmap from image")
        self.image_label.setPixmap(self.pixmap.fromImage(image))

    def origin_color(self):
        for i in range(GrayscaleImageWindow.COLOR_TABLE_SIZE):
            self.image.setColor(i, qRgb(i, i, i))
        self.copy_image(self.image)
        return self

    def reverse(self):
        for i in range(GrayscaleImageWindow.COLOR_TABLE_SIZE):
            color_i = self.image.color(i)
            self.image.setColor(i, qRgb(self.MAX_BRIGHTNESS - qRed(color_i), self.MAX_BRIGHTNESS - qGreen(color_i), self.MAX_BRIGHTNESS - qBlue(color_i)))
        self.copy_image(self.image)
        return self

    def hsl(self):
        angle1 = 0.0
        angle2 = 2.0 * math.pi / 3.0
        angle3 = 4.0 * math.pi / 3.0
        step = 2.0 * math.pi / self.COLOR_TABLE_SIZE
        for i in range(GrayscaleImageWindow.COLOR_TABLE_SIZE):
            self.image.setColor(i, qRgb(int((math.cos(angle1) + 1.0) * self.MAX_BRIGHTNESS / 2.0),
                                        int((math.cos(angle2) + 1.0) * self.MAX_BRIGHTNESS / 2.0),
                                        int((math.cos(angle3) + 1.0) * self.MAX_BRIGHTNESS / 2.0)))
            angle1 += step
            angle2 += step
            angle3 += step
        self.copy_image(self.image)
        return self
    #
    # if mode == "grayscale":
    #     sub_window = GrayscaleImageWindow(self.name, self)
    # else:
    #     sub_window = RgbImageWindow(self.name, self)
    # if sub_window:
    #     for x, y in product(range(self.image.height()), range(self.image.width())):
    #         if not with_neighbors:
    #             pixel = self.image.pixel(x, y)
    #             new_pixel = method(pixel)
    #         else:
    #             new_pixel = method(self.image, x, y)
    #         sub_window.image.setPixel(x, y, new_pixel)
    #     sub_window.update_pixmap(sub_window.image)
    #     return sub_window
    def floyd(self):
        sub_window = GrayscaleImageWindow(self.name, self)
        for x, y in product(range(self.image.height()), range(self.image.width())):
            pixel_index = self.image.pixelIndex(x, y)
            sub_window.image.setPixel(x, y, pixel_index)

        for y in range(self.height() - 1):
            pixel_index = self.image.pixelIndex(0, y)
            level = (pixel_index)

