#!/usr/bin/python
import os
import time

from PIL import Image
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QIcon, QPixmap
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QGridLayout, QPushButton

ICON_SIZE = 130, 130


# Bottom window in the main window
class BWindow(QFrame):
    def __init__(self, parent):
        QFrame.__init__(self, parent)
        self.parent = parent

        self.init_UI()

    def init_UI(self):
        self.setMaximumHeight(141)
        self.rootHbox = QHBoxLayout()
        self.rootHbox.setSpacing(4)
        self.init_vbox_info()
        self.init_vbox_two()

        self.setLayout(self.rootHbox)

    def init_vbox_info(self):
        self.hbox_info = QHBoxLayout()
        self.vbox_info_1 = QVBoxLayout()
        self.vbox_info_1.setAlignment(Qt.AlignCenter)
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
        self.icon_pixmap = QPixmap("./thumbnails/default.jpg")
        self.image_icon_lbl.setPixmap(self.icon_pixmap)
        self.hbox_info.addWidget(self.image_icon_lbl)
        self.hbox_info.addLayout(self.vbox_info_1)
        self.hbox_info.addLayout(self.vbox_info_2)
        self.rootHbox.addLayout(self.hbox_info)

    def wipe_vbox_info(self):
        labels = [self.name_lbl, self.format_lbl, self.size_lbl, self.height_lbl,
            self.width_lbl, self.path_lbl, self.modified_time_lbl, self.created_time_lbl,
            self.color_space_lbl, self.color_profile_lbl]
        for label in labels:
            label.setText(" ")
        l = self.parent.mdiArea.subWindowList()
        if len(self.parent.mdiArea.subWindowList()) == 1:
            self.image_icon_lbl.setPixmap(QPixmap("./thumbnails/default.jpg"))
            print("length: " + str(len(l)))

    def init_vbox_two(self):
        self.frame_two = QFrame()
        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        # self.grid.setRowMinimumHeight(2, 300)
        # self.grid.setRowMinimumHeight(3, 800)
        self.grid.setAlignment(Qt.AlignTop)
        # lbl1 = QLabel('lbl1')
        # lbl2 = QLabel('lbl2')
        # lbl3 = QLabel('lbl3')
        # lbl4 = QLabel('lbl4')
        # lbl5 = QLabel('lbl5')
        # lbl6 = QLabel('lbl6')
        # lbl7 = QLabel('lbl7')
        # lbl8 = QLabel('lbl8')
        # lbl9 = QLabel('lbl9')
        # lbl10 = QLabel('lbl10')
        # lbl11 = QLabel('lbl11')
        # lbl12 = QLabel('lbl12')
        # lbl1.setPixmap(QPixmap('./Icons/warmer.png'))
        # lbl2.setPixmap(QPixmap('./Icons/view.png'))
        # lbl3.setPixmap(QPixmap('./Icons/vintage.png'))
        # lbl4.setPixmap(QPixmap('./Icons/vintage_2.png'))
        # lbl5.setPixmap(QPixmap('./Icons/summer.png'))
        # lbl6.setPixmap(QPixmap('./Icons/pop.png'))
        # lbl7.setPixmap(QPixmap('./Icons/hdr.png'))
        # lbl8.setPixmap(QPixmap('./Icons/cooler.png'))
        # lbl9.setPixmap(QPixmap('./Icons/fade.png'))
        # lbl10.setPixmap(QPixmap('./Icons/sunny.png'))
        # lbl11.setPixmap(QPixmap('./Icons/beam.png'))
        # lbl12.setPixmap(QPixmap('./Icons/chromatic.png'))
        btn1 = QPushButton('warmer')
        btn1.setIcon(QIcon('./Icons/warmer.png'))
        btn2 = QPushButton('view')
        btn2.setIcon(QIcon('./Icons/view.png'))
        btn3 = QPushButton('vintage')
        btn3.setIcon(QIcon('./Icons/vintage.png'))
        btn4 = QPushButton('vintage 2')
        btn4.setIcon(QIcon('./Icons/vintage_2.png'))
        btn5 = QPushButton('summer')
        btn5.setIcon(QIcon('./Icons/summer.png'))
        btn6 = QPushButton('pop')
        btn6.setIcon(QIcon('./Icons/pop.png'))
        btn7 = QPushButton('HDR')
        btn7.setIcon(QIcon('./Icons/hdr.png'))
        btn8 = QPushButton('cooler')
        btn8.setIcon(QIcon('./Icons/cooler.png'))
        btn9 = QPushButton('fade')
        btn9.setIcon(QIcon('./Icons/fade.png'))
        btn10 = QPushButton('sunny')
        btn10.setIcon(QIcon('./Icons/sunny.png'))
        btn11 = QPushButton('beam')
        btn11.setIcon(QIcon('./Icons/beam.png'))
        btn12 = QPushButton('chromatic')
        btn12.setIcon(QIcon('./Icons/chromatic.png'))


        buttons = [btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12]
        for b in buttons:
            b.setIconSize(QSize(80, 40))
            b.setFixedWidth(140)
            b.setStyleSheet("background-color: transparent")

        btn1.clicked.connect(self.set_1)
        btn2.clicked.connect(self.set_2)
        btn3.clicked.connect(self.set_3)
        btn4.clicked.connect(self.set_4)
        btn5.clicked.connect(self.set_5)
        btn6.clicked.connect(self.set_6)
        btn7.clicked.connect(self.set_7)
        btn8.clicked.connect(self.set_8)
        btn9.clicked.connect(self.set_9)
        btn10.clicked.connect(self.set_10)
        btn11.clicked.connect(self.set_11)
        btn12.clicked.connect(self.set_12)

        self.filter_label = QLabel('Filters: Filter 1 Selected')
        self.grid.addWidget(self.filter_label, 1, 1)

        self.apply_filter_button = QPushButton('Apply Filter')
        self.apply_filter_button.setIcon(QIcon('Icons/filter.png'))
        self.apply_filter_button.clicked.connect(self.parent.handler.handle_filter)
        self.grid.addWidget(self.apply_filter_button, 1, 2)

        # self.grid.addWidget(lbl1, 2, 1, Qt.AlignCenter)
        self.grid.addWidget(btn1, 3, 1, Qt.AlignCenter)
        # self.grid.addWidget(lbl2, 2, 2, Qt.AlignCenter)
        self.grid.addWidget(btn2, 3, 2, Qt.AlignCenter)
        # self.grid.addWidget(lbl3, 2, 3, Qt.AlignCenter)
        self.grid.addWidget(btn3, 3, 3, Qt.AlignCenter)
        # self.grid.addWidget(lbl4, 2, 4, Qt.AlignCenter)
        self.grid.addWidget(btn4, 3, 4, Qt.AlignCenter)
        # self.grid.addWidget(lbl5, 2, 5, Qt.AlignCenter)
        self.grid.addWidget(btn5, 3, 5, Qt.AlignCenter)
        # self.grid.addWidget(lbl6, 2, 6, Qt.AlignCenter)
        self.grid.addWidget(btn6, 3, 6, Qt.AlignCenter)
        # self.grid.addWidget(lbl7, 4, 1, Qt.AlignCenter)
        self.grid.addWidget(btn7, 5, 1, Qt.AlignCenter)
        # self.grid.addWidget(lbl8, 4, 2, Qt.AlignCenter)
        self.grid.addWidget(btn8, 5, 2, Qt.AlignCenter)
        # self.grid.addWidget(lbl9, 4, 3, Qt.AlignCenter)
        self.grid.addWidget(btn9, 5, 3, Qt.AlignCenter)
        # self.grid.addWidget(lbl10, 4, 4, Qt.AlignCenter)
        self.grid.addWidget(btn10, 5, 4, Qt.AlignCenter)
        # self.grid.addWidget(lbl11, 4, 5, Qt.AlignCenter)
        self.grid.addWidget(btn11, 5, 5, Qt.AlignCenter)
        # self.grid.addWidget(lbl12, 4, 6, Qt.AlignCenter)
        self.grid.addWidget(btn12, 5, 6, Qt.AlignCenter)

        self.frame_two.setLayout(self.grid)
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

        icon_name = "./thumbnails/" + short_name.replace(".", "@2x.")
        self.generate_icon(file_name, icon_name)

        self.icon_pixmap = QPixmap(icon_name)
        self.icon_pixmap = self.icon_pixmap.scaledToHeight(250)
        self.icon_pixmap = self.icon_pixmap.scaledToWidth(250)
        self.image_icon_lbl.setPixmap(self.icon_pixmap)
        self.image_icon_lbl.setFixedWidth(140)


    def generate_icon(self, file_name, icon_name):
        im = Image.open(file_name)
        im.thumbnail(ICON_SIZE)
        im.save(icon_name)

    def set_1 (self):
        self.parent.filter = 1
        self.filter_label.setText('Filters: Filter 1 Selected')

    def set_2 (self):
        self.parent.filter = 2
        self.filter_label.setText('Filters: Filter 2 Selected')

    def set_3 (self):
        self.parent.filter = 3
        self.filter_label.setText('Filters: Filter 3 Selected')

    def set_4 (self):
        self.parent.filter = 4
        self.filter_label.setText('Filters: Filter 4 Selected')

    def set_5 (self):
        self.parent.filter = 5
        self.filter_label.setText('Filters: Filter 5 Selected')

    def set_6 (self):
        self.parent.filter = 6
        self.filter_label.setText('Filters: Filter 6 Selected')

    def set_7 (self):
        self.parent.filter = 7
        self.filter_label.setText('Filters: Filter 7 Selected')

    def set_8 (self):
        self.parent.filter = 8
        self.filter_label.setText('Filters: Filter 8 Selected')

    def set_9 (self):
        self.parent.filter = 9
        self.filter_label.setText('Filters: Filter 9 Selected')

    def set_10 (self):
        self.parent.filter = 10
        self.filter_label.setText('Filters: Filter 10 Selected')

    def set_11 (self):
        self.parent.filter = 11
        self.filter_label.setText('Filters: Filter 11 Selected')

    def set_12 (self):
        self.parent.filter = 12
        self.filter_label.setText('Filters: Filter 12 Selected')
