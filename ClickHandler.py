#!/usr/bin/python
import json
import os, subprocess, webbrowser
from urllib.error import URLError, HTTPError

import requests
from PIL import Image, ImageGrab
from io import BytesIO
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QInputDialog, QLineEdit

from GrayScaleImageWindow import GrayscaleImageWindow
from RgbImageWindow import RgbImageWindow


class ClickHandler:
    def __init__(self, mw):
        # Container is the main window of the click handler
        self.container = mw

    def handle(self, func):
        if self.container.mdiArea.currentSubWindow():
            try:
                sub_window = func()
                if not sub_window:
                    pass
                    # QMessageBox.information(self.container, "Error", "Unable to add a sub window")
                elif sub_window != self.container.mdiArea.currentSubWindow():
                    self.container.mdiArea.addSubWindow(sub_window)
                    sub_window.show()
            except Exception:
                QMessageBox.information(self, "Error", "Fail to perform action")

    def handle_open(self, relative_path: str = ""):
        if not relative_path:
            my_path = "/Users/Carlistle/Developer/PyCharmWorkspace/CuteImage/Photos_Library_photoslibrary/"
        else:
            my_path = "/Users/Carlistle/Developer/PyCharmWorkspace/CuteImage/Photos_Library_photoslibrary/" + relative_path
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

    def parse_json(self):
        settings = open("./default/userDefault.json")
        settings_text = ''
        for line in settings:
            settings_text += line
        settings.close()
        return json.loads(settings_text)

    def handle_open_for_json(self):
        json_obj = self.parse_json()
        for file_name in list(set(json_obj['open-windows'])):
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

    def open_url_image(self, url="https://upload.wikimedia.org/wikipedia/ru/f/fd/Everything_Has_Changed.png"):
        try:
            if len(url) == 0:
                response = requests.get("https://upload.wikimedia.org/wikipedia/ru/f/fd/Everything_Has_Changed.png")
            else:
                response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            # img.show()
            file_name = "URL image"
            # self.container.lwindow.add_list_item(file_name)
            # self.container.bwindow.update_image_info(file_name)
            # Create a new image window with the option 0
            subwindow = RgbImageWindow(file_name, 0, self.container, img)
            subwindow.update_pixmap(subwindow.image)
            if not subwindow:
                QMessageBox.information(self.container, "Error", "Fail to create a sub window")
            else:
                self.container.mdiArea.addSubWindow(subwindow)
                subwindow.show()
        except HTTPError as e:
            QMessageBox.information(self.container, "HTTP Error: " + str(e.code))
        except URLError as e:
            QMessageBox.information(self.container, "URL Error: ", str(e.args))
        except Exception as e:
            QMessageBox.information(self.container, "Bad URL: " + url, "Bad URL")

    def handle_url(self):
        # https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/777dab94-58be-44c4-884c-aaab499ad7b7/dc8mvdq-2ec9dce4-10d0-4cec-a578-b7015e2669c8.png/v1/fill/w_894,h_894,q_70,strp/taylor_swift_spotify_singles_by_kallumlavigne_dc8mvdq-pre.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTAwMCIsInBhdGgiOiJcL2ZcLzc3N2RhYjk0LTU4YmUtNDRjNC04ODRjLWFhYWI0OTlhZDdiN1wvZGM4bXZkcS0yZWM5ZGNlNC0xMGQwLTRjZWMtYTU3OC1iNzAxNWUyNjY5YzgucG5nIiwid2lkdGgiOiI8PTEwMDAifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.13UmHr_zSjE7W0vDuuhA00E7jatjQROm32DAsg9nON0
        text, okPressed = QInputDialog.getText(self.container, "Open Image from URL", "Image address:", QLineEdit.Normal, "")
        if okPressed:
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
        window_list = []
        for subwindow in self.container.mdiArea.subWindowList():
            window_list.append(subwindow.name)
        json_obj = self.parse_json()
        json_obj["open-windows"] = window_list
        self.save_json(json_obj)
        self.container.mdiArea.closeAllSubWindows()

    def handle_close_event(self):
        window_list = []
        for subwindow in self.container.mdiArea.subWindowList():
            window_list.append(subwindow.name)
        json_obj = self.parse_json()
        json_obj["open-windows"] = window_list
        self.save_json(json_obj)

    def save_json(self, json_obj):
        # save to file
        with open("./default/userDefault.json", "w") as file:
            json.dump(json_obj, file)

    def handle_save(self):
        sub_window = self.container.mdiArea.activeSubWindow()
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            if sub_window:
                file_name = QFileDialog.getSaveFileName(self.container, "Save Image", "Photos_Library_photoslibrary")
                sub_window.image.save(file_name[0])

    def handle_info(self):
        self.handle(self.container.mdiArea.currentSubWindow().info)

    def handle_reverse(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().reverse)
        elif isinstance(self.container.mdiArea.currentSubWindow(), GrayscaleImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().reverse)

    def handle_saturate_red(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().saturate_red)

    def handle_saturate_green(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().saturate_green)

    def handle_saturate_blue(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().saturate_blue)

    def handle_to_grayscale(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().to_grayscale)

    def handle_original_color(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().origin_color)

    def handle_threshold(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().threshold)

    def handle_blur(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().blur)

    def handle_sharpen(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().sharpen)

    def handle_kernel(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().kernel)

    def handle_ccl(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().ccl)

    def handle_hsl(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().hsl)

    def handle_outline(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().outline)

    def handle_smooth(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().smooth)

    def handle_smooth_more(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().smooth_more)

    def handle_detail(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().detail)

    def handle_emboss(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().emboss)

    def handle_edge(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().edge_enhance)

    def handle_edge_more(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().edge_enhance_more)

    def handle_find_edges(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().find_edges)

    def handle_gaussian_blur(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().gaussian_blur)

    def handle_box_blur(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().box_blur)

    def handle_unsharp_mask(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().unsharp_mask)

    def handle_dithering(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().dithering)

    def handle_rank_filter(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().rank_filter)

    def handle_min_filter(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().min_filter)

    def handle_max_filter(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().max_filter)

    def handle_median_filter(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().median_filter)

    def handle_resize(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().resize_img)

    def handle_clipboard(self):
        self.container.clipboardChanged()
        if self.container.clip_board_image != None:
            img = ImageGrab.grabclipboard()
            if img:
                # img.show()
                file_name = "Clipboard Image"
                subwindow = RgbImageWindow(file_name, 0, self.container, img)
                subwindow.update_pixmap(subwindow.image)
                if not subwindow:
                    QMessageBox.information(self, "Error", "Fail to create a sub window")
                else:
                    self.container.mdiArea.addSubWindow(subwindow)
                    subwindow.show()

    def handle_rgb(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().set_rgb)

    def handle_filter(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().filter)

    def handle_custom_filter(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().custom_filter)

    def handle_crop(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().crop)

    def handle_timer(self):
        if isinstance(self.container.mdiArea.currentSubWindow(), RgbImageWindow):
            self.handle(self.container.mdiArea.currentSubWindow().timer)

    def handle_toggle_l(self):
        if self.container.gridLayout.columnMinimumWidth(1) > 200:
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

