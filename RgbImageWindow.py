import subprocess
from itertools import product

from PIL import Image, ImageFilter
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QMdiSubWindow, QLabel, QMessageBox, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage, qRgb, qRed, qGreen, qBlue
import cclabel
import ClockImg
import Filters
from GrayScaleImageWindow import GrayscaleImageWindow
import Converter


class RgbImageWindow(QMdiSubWindow):
    def __init__(self, name="", parent=None, main_win=None, image=None):
        QMdiSubWindow.__init__(self)
        self.name = name
        self.parent = parent
        self.container = main_win
        self.pil_image = image
        self.initUI()
        self.setAttribute(Qt.WA_DeleteOnClose)

    def initUI(self):
        # ShortName only contains the name, not the path
        self.shortName = self.name.split("/")[-1]
        self.setWindowTitle(self.shortName)


        # Create an image
        self.pixmap = QPixmap()
        self.image_label = QLabel()

        if self.pil_image != None:
            print(self.pil_image.format)
            self.image = QImage(self.pil_image.width, self.pil_image.height, QImage.Format_ARGB32)
            # self.image.
            Converter.show_in_window(self.pil_image, self)
            # self.pil_image.show()
        else:
            if self.parent == 0:
                # Create a new image from name
                self.image = QImage(self.name)
                self.is_new_img = False
            else:
                # Create an image from parent with the same dimension
                self.image = QImage(self.parent.image.size(), self.parent.image.format())
                self.is_new_img = True

        if not self.image.isNull():
            self.loaded_image = True
            self.update_pixmap(self.image)
        else:
            pass
            # QMessageBox(self, "Error", "Unable to create a new image in a new window.")

        self.setWidget(self.image_label)
        self.resize(self.pixmap.size())
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def closeEvent(self, event):
        # print("New image:" + str(self.is_new_img))
        # if not self.is_new_img:
        if hasattr(self.container,'lwindow'):
            self.container.lwindow.remove_item(self.name)
        if hasattr(self.container, 'bwindow'):
            self.container.bwindow.wipe_vbox_info()
        # if len(self.container.mdiArea.subWindowList()) == 1:
        #     self.container.mdiArea.setStyleSheet("background-image: url(Icons/empty_background.png);")
        #     self.container.mdiArea.update()
        #     print("Changing background")
        """
        if can_exit:
            event.accept() # let the window close
        else:
            event.ignore()
            
        app = QApplication(sys.argv)
        app.aboutToQuit.connect(myExitHandler) # myExitHandler is a callable
        """

    def info(self):
        p = subprocess.Popen('mdls ' + self.name, stdout=subprocess.PIPE, shell=True)
        (output, _) = p.communicate()
        p_status = p.wait()
        out_str = str(output)
        out_arr = out_str.split('   ')
        for item in out_str:
            item = item.strip()
        QMessageBox.information(self.container, "Info", out_str)

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
                    if not self.on_boarder(self.image, x, y):
                        sub_window.image.setPixel(x, y, new_pixel)
                sub_window.update_pixmap(sub_window.image)
                return sub_window

    def blur(self):
        # def calc_blur(img, x, y):
        #     if self.on_boarder(img, x, y):
        #         # return the unchanged pixel if it's on the boarder
        #         return img.pixel(x, y)
        #     else:
        #         pixel = img.pixel(x, y)
        #         pixel1 = img.pixel(x - 1, y - 1)
        #         pixel2 = img.pixel(x - 1, y)
        #         pixel3 = img.pixel(x - 1, y + 1)
        #         pixel4 = img.pixel(x, y + 1)
        #         pixel5 = img.pixel(x, y - 1)
        #         pixel6 = img.pixel(x + 1, y - 1)
        #         pixel7 = img.pixel(x + 1, y)
        #         pixel8 = img.pixel(x + 1, y + 1)
        #
        #         r_level = (qRed(pixel) + qRed(pixel1) + qRed(pixel2) + qRed(pixel3) + qRed(pixel4) + qRed(pixel5) +
        #                    qRed(pixel6) + qRed(pixel7) + qRed(pixel8)) / 9.0
        #         g_level = (qGreen(pixel) + qGreen(pixel1) + qGreen(pixel2) + qGreen(pixel3) + qGreen(pixel4) + qGreen(
        #             pixel5) + qGreen(pixel6) + qGreen(pixel7) + qGreen(pixel8)) / 9.0
        #         b_level = (qBlue(pixel) + qBlue(pixel1) + qBlue(pixel2) + qBlue(pixel3) + qBlue(pixel4) + qBlue(
        #             pixel5) + qBlue(pixel6) + qBlue(pixel7) + qBlue(pixel8)) / 9.0
        #         return qRgb(r_level, g_level, b_level)
        # return self.traverse_image(calc_blur, with_neighbors=True)
        image = Image.open(self.name)
        # image.show()
        subwindow = RgbImageWindow(self.name, 0, self.container, image.filter(ImageFilter.BLUR))
        subwindow.update_pixmap(subwindow.image)
        if not subwindow:
            QMessageBox.information(self, "Error", "Fail to create a sub window")
        else:
            self.container.mdiArea.addSubWindow(subwindow)
            subwindow.show()

    def gaussian_blur(self):
        image = Image.open(self.name)
        # print("Gaussian level: ", self.container.rwindow.gaussian)
        subwindow = RgbImageWindow(self.name, 0, self.container, image.filter(ImageFilter.GaussianBlur(radius=self.container.rwindow.gaussian)))
        subwindow.update_pixmap(subwindow.image)
        if not subwindow:
            QMessageBox.information(self, "Error", "Fail to create a sub window")
        else:
            self.container.mdiArea.addSubWindow(subwindow)
            subwindow.show()

    def box_blur(self):
        image = Image.open(self.name)
        # print("Gaussian level: ", self.container.rwindow.gaussian)
        subwindow = RgbImageWindow(self.name, 0, self.container, image.filter(ImageFilter.BoxBlur(radius=self.container.rwindow.gaussian)))
        subwindow.update_pixmap(subwindow.image)
        if not subwindow:
            QMessageBox.information(self, "Error", "Fail to create a sub window")
        else:
            self.container.mdiArea.addSubWindow(subwindow)
            subwindow.show()

    def unsharp_mask(self):
        image = Image.open(self.name)
        # print("Params: ", self.container.rwindow.mask)
        try:
            subwindow = RgbImageWindow(self.name, 0, self.container,
                                       image.filter(ImageFilter.UnsharpMask(radius=self.container.rwindow.mask[0],
                                                                            percent=self.container.rwindow.mask[1],
                                                                            threshold=self.container.rwindow.mask[2])))
            subwindow.update_pixmap(subwindow.image)
            if not subwindow:
                QMessageBox.information(self, "Error", "Fail to create a sub window")
            else:
                self.container.mdiArea.addSubWindow(subwindow)
                subwindow.show()
        except Exception:
            QMessageBox.information(self, "Error", "Parameter error")

    def rank_filter(self):
        image = Image.open(self.name)
        # print("Params: ", self.container.rwindow.mask)
        try:
            subwindow = RgbImageWindow(self.name, 0, self.container,
                                       image.filter(ImageFilter.RankFilter(size=self.container.rwindow.filter_size, rank=self.container.rwindow.filter_rank)))
            subwindow.update_pixmap(subwindow.image)
            if not subwindow:
                QMessageBox.information(self, "Error", "Fail to create a sub window")
            else:
                self.container.mdiArea.addSubWindow(subwindow)
                subwindow.show()
        except Exception:
            QMessageBox.information(self, "Error", "Parameter error")

    def min_filter(self):
        image = Image.open(self.name)
        try:
            # print("Params: ", self.container.rwindow.mask)
            subwindow = RgbImageWindow(self.name, 0, self.container,
                                       image.filter(ImageFilter.MinFilter(size=self.container.rwindow.filter_size)))
            subwindow.update_pixmap(subwindow.image)
            if not subwindow:
                QMessageBox.information(self, "Error", "Fail to create a sub window")
            else:
                self.container.mdiArea.addSubWindow(subwindow)
                subwindow.show()
        except Exception:
            QMessageBox.information(self, "Error", "Parameter error")

    def max_filter(self):
        image = Image.open(self.name)
        try:
            # print("Params: ", self.container.rwindow.mask)
            subwindow = RgbImageWindow(self.name, 0, self.container,
                                       image.filter(ImageFilter.MaxFilter(size=self.container.rwindow.filter_size)))
            subwindow.update_pixmap(subwindow.image)
            if not subwindow:
                QMessageBox.information(self, "Error", "Fail to create a sub window")
            else:
                self.container.mdiArea.addSubWindow(subwindow)
                subwindow.show()
        except Exception:
            QMessageBox.information(self, "Error", "Parameter error")

    def median_filter(self):
        image = Image.open(self.name)
        try:
            # print("Params: ", self.container.rwindow.mask)
            subwindow = RgbImageWindow(self.name, 0, self.container,
                                       image.filter(ImageFilter.MedianFilter(size=self.container.rwindow.filter_size)))
            subwindow.update_pixmap(subwindow.image)
            if not subwindow:
                QMessageBox.information(self, "Error", "Fail to create a sub window")
            else:
                self.container.mdiArea.addSubWindow(subwindow)
                subwindow.show()
        except Exception:
            QMessageBox.information(self, "Error", "Parameter error")

    def kernel(self):
        image = Image.open(self.name)
        try:
            # print("Params: ", self.container.rwindow.mask)
            km = []
            for field in self.container.rwindow.idx_fields:
                km.append(field.value())
            print(km)
            print("Scale: ", str(self.container.rwindow.kernel_scale / 10.0) * sum(km))
            k = ImageFilter.Kernel(
                size=(3, 3),
                kernel=km,
                scale=sum(km) * (self.container.rwindow.kernel_scale / 10.0),
                offset=self.container.rwindow.kernel_offset / 10.0 - 1.0
            )
            subwindow = RgbImageWindow(self.name, 0, self.container,
                                       image.filter(k))
            subwindow.update_pixmap(subwindow.image)
            if not subwindow:
                QMessageBox.information(self, "Error", "Fail to create a sub window")
            else:
                self.container.mdiArea.addSubWindow(subwindow)
                subwindow.show()
        except Exception:
            QMessageBox.information(self, "Error", "Parameter error")

    def sharpen(self):
        # def calc_sharpen(img, x, y):
        #     if self.on_boarder(img, x, y):
        #         # return the unchanged pixel if it's on the boarder
        #         return img.pixel(x, y)
        #     else:
        #         pixel = img.pixel(x, y)
        #         pixel1 = img.pixel(x - 1, y - 1)
        #         pixel2 = img.pixel(x - 1, y)
        #         pixel3 = img.pixel(x - 1, y + 1)
        #         pixel4 = img.pixel(x, y + 1)
        #         pixel5 = img.pixel(x, y - 1)
        #         pixel6 = img.pixel(x + 1, y - 1)
        #         pixel7 = img.pixel(x + 1, y)
        #         pixel8 = img.pixel(x + 1, y + 1)
        #
        #         r_level = min(255, (9 * qRed(pixel) - qRed(pixel1) - qRed(pixel2) - qRed(pixel3) - qRed(pixel4)
        #                             - qRed(pixel5) - qRed(pixel6) - qRed(pixel7) - qRed(pixel8)))
        #         g_level = min(255, (9 * qGreen(pixel) - qGreen(pixel1) - qGreen(pixel2) - qGreen(pixel3) - qGreen(
        #             pixel4) - qGreen(pixel5) - qGreen(pixel6) - qGreen(pixel7) - qGreen(pixel8)))
        #         b_level = min(255, (9 * qBlue(pixel) - qBlue(pixel1) - qBlue(pixel2) - qBlue(pixel3) - qBlue(pixel4)
        #                             - qBlue(pixel5) - qBlue(pixel6) - qBlue(pixel7) - qBlue(pixel8)))
        #         return qRgb(r_level, g_level, b_level)
        # return self.traverse_image(calc_sharpen, with_neighbors=True)
        image = Image.open(self.name)
        try:
            # image.show()
            subwindow = RgbImageWindow(self.name, 0, self.container, image.filter(ImageFilter.SHARPEN))
            subwindow.update_pixmap(subwindow.image)
            if not subwindow:
                QMessageBox.information(self, "Error", "Fail to create a sub window")
            else:
                self.container.mdiArea.addSubWindow(subwindow)
                subwindow.show()
        except Exception:
            QMessageBox.information(self, "Error", "Parameter error")


    def outline(self):
        image = Image.open(self.name)
        # image.show()
        try:
            subwindow = RgbImageWindow(self.name, 0, self.container, image.filter(ImageFilter.CONTOUR))
            subwindow.update_pixmap(subwindow.image)
            if not subwindow:
                QMessageBox.information(self, "Error", "Fail to create a sub window")
            else:
                self.container.mdiArea.addSubWindow(subwindow)
                subwindow.show()
        except Exception:
            QMessageBox.information(self, "Error", "Parameter error")
        # def calc_outline(img, x, y):
        #     if self.on_boarder(img, x, y):
        #         # return the unchanged pixel if it's on the boarder
        #         return img.pixel(x, y)
        #     else:
        #         pixel = img.pixel(x, y)
        #         pixel1 = img.pixel(x - 1, y - 1)
        #         pixel2 = img.pixel(x - 1, y)
        #         pixel3 = img.pixel(x - 1, y + 1)
        #         pixel4 = img.pixel(x, y - 1)
        #         pixel5 = img.pixel(x, y + 1)
        #         pixel6 = img.pixel(x + 1, y - 1)
        #         pixel7 = img.pixel(x + 1, y)
        #         pixel8 = img.pixel(x + 1, y + 1)
        #
        #         r_level = min(255,  abs(qRed(pixel) - qRed(pixel1)) +
        #                                abs(qRed(pixel) - qRed(pixel2)) +
        #                                    abs(qRed(pixel) - qRed(pixel3)) +
        #                                        abs(qRed(pixel) - qRed(pixel4)) +
        #                                            abs(qRed(pixel) - qRed(pixel5)) +
        #                                                abs(qRed(pixel) - qRed(pixel6)) +
        #                                                    abs(qRed(pixel) - qRed(pixel7)) +
        #                                                        abs(qRed(pixel) - qRed(pixel8)))
        #         g_level = min(255,  abs(qGreen(pixel) - qGreen(pixel1)) +
        #                                abs(qGreen(pixel) - qGreen(pixel2)) +
        #                                    abs(qGreen(pixel) - qGreen(pixel3)) +
        #                                        abs(qGreen(pixel) - qGreen(pixel4)) +
        #                                            abs(qGreen(pixel) - qGreen(pixel5)) +
        #                                                abs(qGreen(pixel) - qGreen(pixel6)) +
        #                                                    abs(qGreen(pixel) - qGreen(pixel7)) +
        #                                                        abs(qGreen(pixel) - qGreen(pixel8)))
        #         b_level = min(255,  abs(qBlue(pixel) - qBlue(pixel1)) +
        #                                abs(qBlue(pixel) - qBlue(pixel2)) +
        #                                    abs(qBlue(pixel) - qBlue(pixel3)) +
        #                                        abs(qBlue(pixel) - qBlue(pixel4)) +
        #                                            abs(qBlue(pixel) - qBlue(pixel5)) +
        #                                                abs(qBlue(pixel) - qBlue(pixel6)) +
        #                                                    abs(qBlue(pixel) - qBlue(pixel7)) +
        #                                                        abs(qBlue(pixel) - qBlue(pixel8)))
        #         return qRgb(int(r_level), int(g_level), int(b_level))
        #
        # return self.traverse_image(calc_outline, with_neighbors=True)

    def on_boarder(self, img, x, y):
        if x == 0 or x >= (img.width() - 1):
            return True
        elif y == 0 or y >= (img.height() - 1):
            return True
        else:
            return False

    def origin_color(self):
        def calc_origin_color(pixel):
            return qRgb(qRed(pixel), qGreen(pixel), qBlue(pixel))
        return self.traverse_image(calc_origin_color)

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
            gray_level = 0.299 * qRed(pixel) + 0.587 * qGreen(pixel) + 0.114 * qBlue(pixel)
            return qRgb(gray_level, gray_level, gray_level)
        return self.traverse_image(calc_to_grayscale)

    def threshold(self):
        def calc_threshold(pixel):
            if qRed(pixel) > self.container.get_rgb()[0]:
                adjusted_red = 255
            else:
                adjusted_red = 0
            if qGreen(pixel) > self.container.get_rgb()[1]:
                adjusted_green = 255
            else:
                adjusted_green = 0
            if qBlue(pixel) > self.container.get_rgb()[2]:
                adjusted_blue = 255
            else:
                adjusted_blue = 0
            return qRgb(adjusted_red, adjusted_green, adjusted_blue)

        if hasattr(self.container, 'rgb'):
            return self.traverse_image(calc_threshold)
        else:
            pass

    def crop(self):
        image = Image.open(self.name)
        # image.show()
        width, height = image.size
        border = (max(0, self.container.xy[0]), max(0, self.container.xy[1]),
                  min(width, self.container.xy[0] + self.container.hw[1]),
                  min(height, self.container.xy[1] + self.container.hw[0]))
        # image.crop(border).show()
        subwindow = RgbImageWindow(self.name, 0, self.container, image.crop(border))
        subwindow.update_pixmap(subwindow.image)
        if not subwindow:
            QMessageBox.information(self, "Error", "Fail to create a sub window")
        else:
            self.container.mdiArea.addSubWindow(subwindow)
            subwindow.show()
        # sub_window = RgbImageWindow(self.name, self)
        # rect = QRect(max(self.container.xy[0], 0), max(self.container.xy[1], 0),
        #              min(self.container.hw[0], sub_window.image.height()),
        #              max(self.container.hw[1], sub_window.image.width()))
        # sub_window.image = sub_window.image.copy(rect)
        # sub_window.update_pixmap(sub_window.image)
        # return sub_window
        # # QPixmap original('image.png');
        # # QPixmap cropped = original.copy(rect);

    def set_rgb(self):
        def calc_set_rgb(pixel):
            if hasattr(self.container,'rgb'):
                return qRgb(qRed(pixel) * self.container.rgb[0] / 255,
                            qGreen(pixel) * self.container.rgb[1] / 255,
                            qBlue(pixel) * self.container.rgb[0] / 255)
            else:
                return qRgb(255, 255, 255)

        return self.traverse_image(calc_set_rgb)

    def filter(self):
        if hasattr(self.container, 'filter'):
            filter_number = self.container.filter
            r_lambda, g_lambda, b_lambda = Filters.FILTERS[filter_number - 1]
            def calc_filter(pixel):
                return qRgb(self.fit_range(r_lambda(qRed(pixel))), self.fit_range(g_lambda(qGreen(pixel))),
                            self.fit_range(b_lambda(qBlue(pixel))))
            return self.traverse_image(calc_filter)

    def custom_filter(self):
        r1 = self.container.rwindow.rgb_input[0].value()
        g1 = self.container.rwindow.rgb_input[1].value()
        b1 = self.container.rwindow.rgb_input[2].value()
        r2 = self.container.rwindow.rgb_input[3].value()
        g2 = self.container.rwindow.rgb_input[4].value()
        b2 = self.container.rwindow.rgb_input[5].value()
        r_lambda, g_lambda, b_lambda = [(lambda r: r * r1 + r2), (lambda g: g * g1 + g2), (lambda b: b * b1 + b2)]
        def calc_filter(pixel):
            return qRgb(self.fit_range(r_lambda(qRed(pixel))), self.fit_range(g_lambda(qGreen(pixel))),
                        self.fit_range(b_lambda(qBlue(pixel))))
        return self.traverse_image(calc_filter)

    def fit_range(self, i):
        if i > 255:
            return 255
        elif i < 0:
            return 0
        else:
            return i

    def ccl(self):
        cclabel.ccl(self.name)

    def timer(self):
        ClockImg.start(self.name, self)

    def dithering(self):
        image = Image.open(self.name)
        # image.show()
        try:
            subwindow = RgbImageWindow(self.name, 0, self.container, image.convert(dither=Image.FLOYDSTEINBERG))
            subwindow.update_pixmap(subwindow.image)
            if not subwindow:
                QMessageBox.information(self, "Error", "Fail to create a sub window")
            else:
                self.container.mdiArea.addSubWindow(subwindow)
                subwindow.show()
        except Exception:
            QMessageBox.information(self, "Error", "Parameter error")
        # if self.loaded_image:
        #     sub_window = RgbImageWindow(self.name, self)
        #     if sub_window:
        #         for x, y in product(range(1, self.image.height() - 1), range(1, self.image.width() - 1)):
        #             pixel = self.image.pixel(x, y)
        #             gray_scale = 0.3 * qRed(pixel) + 0.59 * qGreen(pixel) + 0.11 * qBlue(pixel)
        #             sub_window.image.setPixel(x, y, qRgb(gray_scale, gray_scale, gray_scale))
        #             """
        #                      P      7 P1
        #             3 P2   5 P3     1 P4
        #             """
        #             pixel = self.image.pixel(x, y)
        #             pixel1 = self.image.pixel(x + 1, y)
        #             pixel2 = self.image.pixel(x - 1, y + 1)
        #             pixel3 = self.image.pixel(x, y + 1)
        #             pixel4 = self.image.pixel(x + 1, y + 1)
        #             newR = round(4 * qRed(pixel) / 255) * (255 / 4)
        #             newG = round(4 * qGreen(pixel) / 255) * (255 / 4)
        #             newB = round(4 * qBlue(pixel) / 255) * (255 / 4)
        #             errRGB = qRed(pixel) - newR, qGreen(pixel) - newG, qBlue(pixel) - newB
        #             if not self.on_boarder(self.image, x + 1, y):
        #                 sub_window.image.setPixel(x + 1, y, qRgb(qRed(pixel1) + errRGB[0] * 7.0 / 16.0,
        #                                                      qGreen(pixel1) + errRGB[1] * 7.0 / 16.0,
        #                                                      qBlue(pixel1) + errRGB[2] * 7.0 / 16.0))
        #
        #             if not self.on_boarder(self.image, x - 1, y + 1):
        #                 sub_window.image.setPixel(x - 1, y + 1, qRgb(qRed(pixel2) + errRGB[0] * 3.0 / 16.0,
        #                                                      qGreen(pixel2) + errRGB[1] * 3.0 / 16.0,
        #                                                      qBlue(pixel2) + errRGB[2] * 3.0 / 16.0))
        #
        #             if not self.on_boarder(self.image, x, y + 1):
        #                 sub_window.image.setPixel(x, y + 1, qRgb(qRed(pixel3) + errRGB[0] * 5.0 / 16.0,
        #                                                      qGreen(pixel3) + errRGB[1] * 5.0 / 16.0,
        #                                                      qBlue(pixel3) + errRGB[2] * 5.0 / 16.0))
        #
        #             if not self.on_boarder(self.image, x + 1, y + 1):
        #                 sub_window.image.setPixel(x + 1, y + 1, qRgb(qRed(pixel4) + errRGB[0] * 1.0 / 16.0,
        #                                                      qGreen(pixel4) + errRGB[1] * 1.0 / 16.0,
        #                                                      qBlue(pixel4) + errRGB[1] * 1.0 / 16.0))
        #
        #             if not self.on_boarder(self.image, x, y):
        #                 sub_window.image.setPixel(x, y, qRgb(newR, newG, newB))
        #             else:
        #                 sub_window.image.setPixel(x, y, qRgb(255, 255, 255))
        #     sub_window.update_pixmap(sub_window.image)
        #     return sub_window

    def smooth(self):
        image = Image.open(self.name)
        try:
            # image.show()
            subwindow = RgbImageWindow(self.name, 0, self.container, image.filter(ImageFilter.SMOOTH))
            subwindow.update_pixmap(subwindow.image)
            if not subwindow:
                QMessageBox.information(self, "Error", "Fail to create a sub window")
            else:
                self.container.mdiArea.addSubWindow(subwindow)
                subwindow.show()
        except Exception:
            QMessageBox.information(self, "Error", "Parameter error")

    def resize_img(self):
        image = Image.open(self.name)
        # image.show()
        s = int(image.width * self.container.rwindow.width_percent.value() / 100.0),\
            int(image.height * self.container.rwindow.height_percent.value() / 100.0)
        print(s)
        subwindow = RgbImageWindow(self.name, 0, self.container, image.resize(s))
        subwindow.update_pixmap(subwindow.image)
        if not subwindow:
            QMessageBox.information(self, "Error", "Fail to create a sub window")
        else:
            self.container.mdiArea.addSubWindow(subwindow)
            subwindow.show()

    def detail(self):
        image = Image.open(self.name)
        try:
            # image.show()
            subwindow = RgbImageWindow(self.name, 0, self.container, image.filter(ImageFilter.DETAIL))
            subwindow.update_pixmap(subwindow.image)
            if not subwindow:
                QMessageBox.information(self, "Error", "Fail to create a sub window")
            else:
                self.container.mdiArea.addSubWindow(subwindow)
                subwindow.show()
        except Exception:
            QMessageBox.information(self, "Error", "Parameter error")

    def emboss(self):
        image = Image.open(self.name)
        try:
            # image.show()
            subwindow = RgbImageWindow(self.name, 0, self.container, image.filter(ImageFilter.EMBOSS))
            subwindow.update_pixmap(subwindow.image)
            if not subwindow:
                QMessageBox.information(self, "Error", "Fail to create a sub window")
            else:
                self.container.mdiArea.addSubWindow(subwindow)
                subwindow.show()
        except Exception:
            QMessageBox.information(self, "Error", "Parameter error")

    def smooth_more(self):
        image = Image.open(self.name)
        try:
            # image.show()
            subwindow = RgbImageWindow(self.name, 0, self.container, image.filter(ImageFilter.SMOOTH_MORE))
            subwindow.update_pixmap(subwindow.image)
            if not subwindow:
                QMessageBox.information(self, "Error", "Fail to create a sub window")
            else:
                self.container.mdiArea.addSubWindow(subwindow)
                subwindow.show()
        except Exception:
            QMessageBox.information(self, "Error", "Parameter error")

    def edge_enhance(self):
        image = Image.open(self.name)
        try:
            # image.show()
            subwindow = RgbImageWindow(self.name, 0, self.container, image.filter(ImageFilter.EDGE_ENHANCE))
            subwindow.update_pixmap(subwindow.image)
            if not subwindow:
                QMessageBox.information(self, "Error", "Fail to create a sub window")
            else:
                self.container.mdiArea.addSubWindow(subwindow)
                subwindow.show()
        except Exception:
            QMessageBox.information(self, "Error", "Parameter error")

    def edge_enhance_more(self):
        image = Image.open(self.name)
        # image.show()
        try:
            subwindow = RgbImageWindow(self.name, 0, self.container, image.filter(ImageFilter.EDGE_ENHANCE_MORE))
            subwindow.update_pixmap(subwindow.image)
            if not subwindow:
                QMessageBox.information(self, "Error", "Fail to create a sub window")
            else:
                self.container.mdiArea.addSubWindow(subwindow)
                subwindow.show()
        except Exception:
            QMessageBox.information(self, "Error", "Parameter error")

    def find_edges(self):
        image = Image.open(self.name)
        try:
            # image.show()
            subwindow = RgbImageWindow(self.name, 0, self.container, image.filter(ImageFilter.FIND_EDGES))
            subwindow.update_pixmap(subwindow.image)
            if not subwindow:
                QMessageBox.information(self, "Error", "Fail to create a sub window")
            else:
                self.container.mdiArea.addSubWindow(subwindow)
                subwindow.show()
        except Exception:
            QMessageBox.information(self, "Error", "Parameter error")

    def hsl(self):
        pass
        # angle1 = 0.0
        # angle2 = 2.0 * math.pi / 3.0
        # angle3 = 4.0 * math.pi / 3.0
        # pas = 2.0 * math.pi / FenetreFilleTC.TAILLE_TDC
        # for i in range(FenetreFilleTC.TAILLE_TDC):
        #     self.image.setColor(i, qRgb(int((math.cos(angle1) + 1.0) * FenetreFilleTC.LUM_MAX / 2.0),
        #                                 int((math.cos(angle2) + 1.0) * FenetreFilleTC.LUM_MAX / 2.0),
        #                                 int((math.cos(angle3) + 1.0) * FenetreFilleTC.LUM_MAX / 2.0)))
        #     angle1 = angle1 + pas
        #     angle2 = angle2 + pas
        #     angle3 = angle3 + pas
        # # Recopie de l'image avec la nouvelle table des couleurs dans la fenêtre
        # self.recopieImage(self.image)
        # return (self)
