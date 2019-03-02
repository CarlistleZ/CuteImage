#!/usr/bin/python
import os
import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QIcon, QPixmap
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout


# Bottom window in the main window
class BWindow(QFrame):
    def __init__(self, parent):
        QFrame.__init__(self, parent)
        self.parent = parent

        self.init_UI()

    def init_UI(self):
        self.rootHbox = QHBoxLayout()

        self.init_vbox_info()
        self.init_vbox_two()

        self.setLayout(self.rootHbox)

    def init_vbox_info(self):
        self.hbox_info = QHBoxLayout()
        self.vbox_info_1 = QVBoxLayout()
        self.vbox_info_1.setAlignment(Qt.AlignTop)
        self.vbox_info_2 = QVBoxLayout()
        self.vbox_info_2.setAlignment(Qt.AlignTop)

        self.name_lbl = QLabel("")
        self.format_lbl = QLabel("")
        self.size_lbl = QLabel("")
        self.height_lbl = QLabel("")
        self.width_lbl = QLabel("")
        self.path_lbl = QLabel("")
        self.modified_time_lbl = QLabel("")
        self.created_time_lbl = QLabel("")
        self.color_space_lbl = QLabel("")
        self.color_profile_lbl = QLabel("")
        self.vbox_info_1.addWidget(self.name_lbl)
        self.vbox_info_1.addWidget(self.height_lbl)
        self.vbox_info_1.addWidget(self.width_lbl)
        self.vbox_info_1.addWidget(self.size_lbl)
        self.vbox_info_1.addWidget(self.format_lbl)
        self.vbox_info_2.addWidget(self.path_lbl)
        self.vbox_info_2.addWidget(self.modified_time_lbl)
        self.vbox_info_2.addWidget(self.created_time_lbl)
        self.vbox_info_2.addWidget(self.color_space_lbl)
        self.vbox_info_2.addWidget(self.color_profile_lbl)

        self.image_icon_lbl = QLabel()
        self.pixmap = QPixmap("./thumbnails/default.jpg")
        self.pixmap.scaledToHeight(130)
        self.pixmap.scaledToWidth(130)
        self.image_icon_lbl.setPixmap(self.pixmap)
        self.hbox_info.addWidget(self.image_icon_lbl)
        self.hbox_info.addLayout(self.vbox_info_1)
        self.hbox_info.addLayout(self.vbox_info_2)
        self.rootHbox.addLayout(self.hbox_info)

    def init_vbox_two(self):
        self.frame_two = QFrame()
        self.vbox_two = QVBoxLayout()
        self.vbox_two.setAlignment(Qt.AlignTop)
        lbl = QLabel("Vbox two")
        self.vbox_two.addWidget(lbl)


        self.frame_two.setLayout(self.vbox_two)
        self.rootHbox.addWidget(self.frame_two)

    def update_image_info(self, file_name):
        tmp_image = QImage(file_name)
        if tmp_image.isNull():
            return

        short_name = file_name.split("/")[-1]
        self.name_lbl.setText("Name: " + short_name)
        img_format = short_name.split(".")[-1]
        self.format_lbl.setText("Format: " + img_format + " image")
        self.size_lbl.setText("Size: " + str(int(os.path.getsize(file_name)/1024)) + "kB")
        self.height_lbl.setText("Height: " + str(tmp_image.height()))
        self.width_lbl.setText("Width: " + str(tmp_image.width()))
        self.modified_time_lbl.setText("Created: " + time.ctime(os.path.getmtime(file_name)))
        self.created_time_lbl.setText("Modified: " + time.ctime(os.path.getatime(file_name)))
        self.color_space_lbl.setText("Color space: RGB")
        self.color_profile_lbl.setText("Color profile: sRGB IEC61966-2.1")
        self.path_lbl.setText("Where: Pictures/" + file_name.split("Photos_Library_photoslibrary/")[-1])
        self.pixmap = QPixmap("./thumbnails/" + short_name.replace(".", "@2x."))
        self.image_icon_lbl.setPixmap(self.pixmap)
        self.pixmap.scaledToHeight(130)
        self.pixmap.scaledToWidth(130)




