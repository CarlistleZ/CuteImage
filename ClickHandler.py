#!/usr/bin/python
import os, subprocess, webbrowser
import urllib.request

from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QInputDialog, QLineEdit

# from MainWindow import MainWindow
from GrayScaleImageWindow import GrayscaleImageWindow
from RgbImageWindow import RgbImageWindow


class ClickHandler:
    def __init__(self, mw):
        # Container is the main window of the click handler
        self.container = mw

    def handle(self, func):
        if self.container.mdiArea.currentSubWindow():
            sub_window = func()
            if not sub_window:
                QMessageBox.information(self.container, "Error", "Unable to add a sub window")
            elif sub_window != self.container.mdiArea.currentSubWindow():
                self.container.mdiArea.addSubWindow(sub_window)
                sub_window.show()

    def handle_open(self, relative_path: str = ""):
        if not relative_path:
            my_path = "./Photos_Library_photoslibrary/"
        else:
            my_path = "./Photos_Library_photoslibrary/" + relative_path
        file_name = QFileDialog.getOpenFileName(self.container, "Choose an image file", my_path)
        if os.path.isfile(file_name[0]):
            image = QImage(file_name[0])
            if not image.isNull():
                self.container.lwindow.add_list_item(file_name[0])
                self.container.bwindow.update_image_info(file_name[0])
                # Create a new image window with the option 0
                if image.format() == QImage.Format_Indexed8:
                    # Create a gray scale image
                    subwindow = GrayscaleImageWindow(file_name[0], 0, self.container)
                else:
                    # Create a rgb color image
                    subwindow = RgbImageWindow(file_name[0], 0, self.container)

                if not subwindow:
                    QMessageBox.information(self, "Error", "Fail to create a sub window")
                else:
                    self.container.mdiArea.addSubWindow(subwindow)
                    subwindow.show()

    def handle_open_for_test(self):
        file_name = "/Users/Carlistle/Developer/PyCharmWorkspace/CuteImage/Photos_Library_photoslibrary/red_small.jpeg"
        if os.path.isfile(file_name):
            image = QImage(file_name)
            if not image.isNull():
                self.container.lwindow.add_list_item(file_name)
                self.container.bwindow.update_image_info(file_name)
                # Create a new image window with the option 0
                if image.format() == QImage.Format_Indexed8:
                    # Create a gray scale image
                    subwindow = GrayscaleImageWindow(file_name, 0, self.container)
                else:
                    # Create a rgb color image
                    subwindow = RgbImageWindow(file_name, 0, self.container)

                if not subwindow:
                    QMessageBox.information(self, "Error", "Fail to create a sub window")
                else:
                    self.container.mdiArea.addSubWindow(subwindow)
                    subwindow.show()

    def open_url_image(self, url):
        try:
            data = urllib.request.urlopen(url).read()
            image = QImage()
            image.loadFromData(data)
            if not image.isNull():
                if len(url) > 20:
                    file_name = 'URL:' + url[20]
                else:
                    file_name = 'URL:' + url
                self.container.lwindow.add_list_item(file_name)
                self.container.bwindow.update_image_info(file_name)
                # Create a new image window with the option 0
                if image.format() == QImage.Format_Indexed8:
                    # Create a gray scale image
                    subwindow = GrayscaleImageWindow(file_name, 0, self.container)
                else:
                    # Create a rgb color image
                    subwindow = RgbImageWindow(file_name, 0, self.container)

                if not subwindow:
                    QMessageBox.information(self, "Error", "Fail to create a sub window")
                else:
                    self.container.mdiArea.addSubWindow(subwindow)
                    subwindow.show()
        except:
            print("Error while opening URL: " + url)

    def handle_url(self):
        text, okPressed = QInputDialog.getText(self.container, "Open Image from URL", "Image address:", QLineEdit.Normal, "")
        if okPressed and text != '':
            self.open_url_image(text)

    def openWithPath(self, path_name):
        self.handle_open(path_name)

    def handle_finder(self):
        my_path = "./Photos_Library_photoslibrary/"
        subprocess.check_call(['open', '--', my_path])

    def handle_camera(self):
        os.system('open -a FaceTime.app')

    def handle_open_with_app(self):
        if isinstance(self.container.mdiArea.activeSubWindow(), RgbImageWindow) or \
                isinstance(self.container.mdiArea.activeSubWindow(), GrayscaleImageWindow):
            my_path =  self.container.mdiArea.activeSubWindow().name
            print(my_path + " is file? " + str(os.path.isfile(my_path)))
            if os.path.isfile(my_path):
                subprocess.check_call(['open', '--', my_path])

    def handle_instagram(self):
        webbrowser.open('https://www.instagram.com', new=0, autoraise=True)

    def handle_twitter(self):
        webbrowser.open('https://twitter.com', new=0, autoraise=True)

    def handle_snapchat(self):
        webbrowser.open('https://www.snapchat.com', new=0, autoraise=True)

    def handle_close_all(self):
        self.container.mdiArea.closeAllSubWindows()

    def handle_save(self):
        pass

    def handle_info(self):
        pass

    def handle_reverse(self):
        self.handle(self.container.mdiArea.currentSubWindow().reverse)

    def handle_saturate_red(self):
        self.handle(self.container.mdiArea.currentSubWindow().saturate_red)

    def handle_saturate_green(self):
        self.handle(self.container.mdiArea.currentSubWindow().saturate_green)

    def handle_saturate_blue(self):
        self.handle(self.container.mdiArea.currentSubWindow().saturate_blue)

    def handle_to_grayscale(self):
        self.handle(self.container.mdiArea.currentSubWindow().to_grayscale)

    def handle_original_color(self):
        self.handle(self.container.mdiArea.currentSubWindow().origin_color)

    def handle_threshold(self):
        self.handle(self.container.mdiArea.currentSubWindow().threshold)

    def handle_blur(self):
        self.handle(self.container.mdiArea.currentSubWindow().blur)

    def handle_sharpen(self):
        self.handle(self.container.mdiArea.currentSubWindow().sharpen)

    def handle_ccl(self):
        self.handle(self.container.mdiArea.currentSubWindow().ccl)

    def handle_hsl(self):
        self.handle(self.container.mdiArea.currentSubWindow().hsl)

    def handle_outline(self):
        pass

    def handle_floyd(self):
        pass

    def handle_clipboard(self):
        self.container.clipboardChanged()

    def handle_rgb(self):
        self.handle(self.container.mdiArea.currentSubWindow().set_rgb)

    def handle_filter(self):
        self.handle(self.container.mdiArea.currentSubWindow().filter)

    def handle_crop(self):
        self.handle(self.container.mdiArea.currentSubWindow().crop)

    def handle_timer(self):
        self.handle(self.container.mdiArea.currentSubWindow().timer)

    def handle_toggle_l(self):
        if  self.container.gridLayout.columnMinimumWidth(1) > 200:
            self.container.gridLayout.setColumnMinimumWidth(1, 1)
            self.container.lwindow.hide()
            self.container.gridLayout.removeWidget(self.container.lwindow)
        else:
            self.container.gridLayout.setColumnMinimumWidth(1, 220)
            self.container.lwindow.show()
            self.container.gridLayout.addWidget(self.container.lwindow, 1, 1)

    def handle_toggle_r(self):
        if self.container.gridLayout.columnMinimumWidth(3) > 200:
            self.container.gridLayout.setColumnMinimumWidth(3, 1)
            self.container.rwindow.hide()
            self.container.gridLayout.removeWidget(self.container.rwindow)
        else:
            self.container.gridLayout.setColumnMinimumWidth(3, 220)
            self.container.rwindow.show()
            self.container.gridLayout.addWidget(self.container.rwindow, 1, 3)

    def handle_toggle_b(self):
        if self.container.gridLayout.rowMinimumHeight(2) > 120:
            self.container.gridLayout.setRowMinimumHeight(2, 1)
            self.container.bwindow.hide()
            self.container.gridLayout.removeWidget(self.container.bwindow)
        else:
            self.container.gridLayout.setRowMinimumHeight(2, 140)
            self.container.bwindow.show()
            self.container.gridLayout.addWidget(self.container.bwindow, 2, 1, 1, 3)

