#!/usr/bin/python
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QTabWidget, QWidget, QPushButton, QSlider, QSpinBox


# Right window in the main window
import MainWindow


class RWindow(QFrame):
    def __init__(self, parent):
        QFrame.__init__(self, parent)
        self.parent = parent
        self.rgb = [128, 128, 128]
        self.xy = [0, 0]
        self.hw = [0, 0]
        self.init_ui()

    def init_ui(self):
        self.rootVbox = QVBoxLayout()
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab1, "Values")
        self.tabs.addTab(self.tab2, "Transformations")

        self.init_tab1()
        self.init_tab2()

        self.rootVbox.addWidget(self.tabs)
        self.setLayout(self.rootVbox)



    def indicateClosedWindow(self, window_name):
        self.lbl2.setText(self.lbl2.text() + "\nYou closed "+window_name+" !")

    def init_tab1(self):
        self.tab1.layout = QVBoxLayout(self)
        self.tab1.layout.setAlignment(Qt.AlignTop)
        self.tab1.layout.setSpacing(8)

        self.init_rgb()
        self.init_coordinates()

        self.tab1.setLayout(self.tab1.layout)

    def init_tab2(self):
        # TODO
        self.tab2.layout = QVBoxLayout(self)
        self.tab2.layout.setAlignment(Qt.AlignTop)
        self.tab2.layout.setSpacing(12)
        self.add_trans_buttons()
        self.tab2.setLayout(self.tab2.layout)

    def add_trans_buttons(self):
        self.tab2.layout.addWidget(QLabel("Group 1:"))
        btn1 = QPushButton('Original Color')
        btn1.setIcon(QIcon('Icons/origin.png'))
        btn1.clicked.connect(self.parent.handler.handle_original_color)
        self.tab2.layout.addWidget(btn1)

        btn2 = QPushButton('Reverse')
        btn2.setIcon(QIcon('Icons/reverse.png'))
        btn2.clicked.connect(self.parent.handler.handle_reverse)
        self.tab2.layout.addWidget(btn2)

        btn3 = QPushButton('Gray Scale')
        btn3.setIcon(QIcon('Icons/to_grayscale.png'))
        btn3.clicked.connect(self.parent.handler.handle_to_grayscale)
        self.tab2.layout.addWidget(btn3)

        self.tab2.layout.addWidget(QLabel("Group 2:"))

        btn4 = QPushButton('Saturate In Red')
        btn4.setIcon(QIcon('Icons/saturate_red.png'))
        btn4.clicked.connect(self.parent.handler.handle_saturate_red)
        self.tab2.layout.addWidget(btn4)

        btn5 = QPushButton('Saturate In Green')
        btn5.setIcon(QIcon('Icons/saturate_green.png'))
        btn5.clicked.connect(self.parent.handler.handle_saturate_green)
        self.tab2.layout.addWidget(btn5)

        btn6 = QPushButton('Saturate In Blue')
        btn6.setIcon(QIcon('Icons/saturate_blue.png'))
        btn6.clicked.connect(self.parent.handler.handle_saturate_blue)
        self.tab2.layout.addWidget(btn6)

        self.tab2.layout.addWidget(QLabel("Group 3:"))

        btn7 = QPushButton('Threshold')
        btn7.setIcon(QIcon('Icons/threshold.png'))
        btn7.clicked.connect(self.parent.handler.handle_threshold)
        self.tab2.layout.addWidget(btn7)

        btn8 = QPushButton('Blur')
        btn8.setIcon(QIcon('Icons/blur.png'))
        btn8.clicked.connect(self.parent.handler.handle_blur)
        self.tab2.layout.addWidget(btn8)

        btn9 = QPushButton('Sharpen')
        btn9.setIcon(QIcon('Icons/sharpen.png'))
        btn9.clicked.connect(self.parent.handler.handle_sharpen)
        self.tab2.layout.addWidget(btn9)

        self.tab2.layout.addWidget(QLabel("Group 4:"))

        btn10 = QPushButton('Object Labeling')
        btn10.setIcon(QIcon('Icons/CCL.png'))
        btn10.clicked.connect(self.parent.handler.handle_ccl)
        self.tab2.layout.addWidget(btn10)


        btn12 = QPushButton('Outline Detection')
        btn12.setIcon(QIcon('Icons/outline.png'))
        btn12.clicked.connect(self.parent.handler.handle_outline)
        self.tab2.layout.addWidget(btn12)

        btn17 = QPushButton('Dithering')
        btn17.setIcon(QIcon('Icons/floyd.png'))
        btn17.clicked.connect(self.parent.handler.handle_dithering)
        self.tab2.layout.addWidget(btn17)

        self.tab2.layout.addWidget(QLabel("Group 5:"))

        btn13 = QPushButton('Filter')
        btn13.setIcon(QIcon('Icons/filter.png'))
        btn13.clicked.connect(self.parent.handler.handle_filter)
        self.tab2.layout.addWidget(btn13)

        btn14 = QPushButton('RGB')
        btn14.setIcon(QIcon('Icons/rgb.png'))
        btn14.clicked.connect(self.parent.handler.handle_rgb)
        self.tab2.layout.addWidget(btn14)

        btn15 = QPushButton('Crop')
        btn15.setIcon(QIcon('Icons/crop.png'))
        btn15.clicked.connect(self.parent.handler.handle_crop)
        self.tab2.layout.addWidget(btn15)

        btn16 = QPushButton('Timer')
        btn16.setIcon(QIcon('Icons/timer.png'))
        btn16.clicked.connect(self.parent.handler.handle_timer)
        self.tab2.layout.addWidget(btn16)

    def init_rgb(self):
        r_level_label = QLabel("Red Level:")
        self.tab1.layout.addWidget(r_level_label)
        self.r_level = QSlider(Qt.Horizontal)
        self.r_level.setTickPosition(QSlider.TicksBelow)
        self.r_level.setTickInterval(64)
        self.r_level.setMinimum(0)
        self.r_level.setMaximum(255)
        self.r_level.setValue(128)
        self.tab1.layout.addWidget(self.r_level)
        self.r_level.valueChanged.connect(self.change_r)

        g_level_label = QLabel("Green Level:")
        self.tab1.layout.addWidget(g_level_label)
        self.g_level = QSlider(Qt.Horizontal)
        self.g_level.setTickPosition(QSlider.TicksBelow)
        self.g_level.setTickInterval(64)
        self.g_level.setMinimum(0)
        self.g_level.setMaximum(255)
        self.g_level.setValue(128)
        self.tab1.layout.addWidget(self.g_level)
        self.g_level.valueChanged.connect(self.change_g)

        b_level_label = QLabel("Blue Level:")
        self.tab1.layout.addWidget(b_level_label)
        self.b_level = QSlider(Qt.Horizontal)
        self.b_level.setTickPosition(QSlider.TicksBelow)
        self.b_level.setTickInterval(64)
        self.b_level.setMinimum(0)
        self.b_level.setMaximum(255)
        self.b_level.setValue(128)
        self.tab1.layout.addWidget(self.b_level)
        self.b_level.valueChanged.connect(self.change_b)

        self.rgb_label = QLabel("R: 128, G: 128, B:128")
        self.tab1.layout.addWidget(self.rgb_label)
        self.hex_label = QLabel("HEX: 0x808080")
        self.tab1.layout.addWidget(self.hex_label)
        self.set_rgb = QPushButton("Set RGB")
        # self.set_rgb.clicked.connect(self.setRgbClicked)
        self.tab1.layout.addWidget(self.set_rgb)

        self.percent_label = QLabel("R: 50%, G:50%, B: 50%")
        self.tab1.layout.addWidget(self.percent_label)
        self.set_percent = QPushButton("Set Percent")
        self.set_percent.clicked.connect(self.setPercentClicked)
        self.tab1.layout.addWidget(self.set_percent)

    def init_coordinates(self):
        self.tab1.layout.addWidget(QLabel(" "))
        x_label = QLabel("X Value:")
        self.tab1.layout.addWidget(x_label)
        self.line_x = QSpinBox()
        self.line_x.setMinimum(0)
        self.line_x.setMaximum(1000)
        self.line_x.setValue(0)
        self.line_x.setSingleStep(10)
        self.line_x.valueChanged.connect(self.x_changed)
        self.tab1.layout.addWidget(self.line_x)

        y_label = QLabel("Y Value:")
        self.tab1.layout.addWidget(y_label)
        self.line_y = QSpinBox()
        self.line_y.setMinimum(0)
        self.line_y.setMaximum(1000)
        self.line_y.setValue(0)
        self.line_y.setSingleStep(10)
        self.line_y.valueChanged.connect(self.y_changed)
        self.tab1.layout.addWidget(self.line_y)

        height_label = QLabel("Width:")
        self.tab1.layout.addWidget(height_label)
        self.line_height = QSpinBox()
        self.line_height.setMinimum(0)
        self.line_height.setMaximum(1000)
        self.line_height.setValue(200)
        self.line_height.setSingleStep(10)
        self.line_height.valueChanged.connect(self.h_changed)
        self.tab1.layout.addWidget(self.line_height)

        width_label = QLabel("Height:")
        self.tab1.layout.addWidget(width_label)
        self.line_width = QSpinBox()
        self.line_width.setMinimum(0)
        self.line_width.setMaximum(1000)
        self.line_width.setValue(200)
        self.line_width.setSingleStep(10)
        self.line_width.valueChanged.connect(self.w_changed)
        self.tab1.layout.addWidget(self.line_width)

        self.set_coord = QPushButton("Set")
        self.set_coord.clicked.connect(self.setCoordClicked)
        self.tab1.layout.addWidget(self.set_coord)

        self.tab1.layout.addWidget(QLabel(" "))
        btn1 = QPushButton('Clipboard')
        btn1.setIcon(QIcon('Icons/clipboard.png'))
        btn1.clicked.connect(self.parent.handler.handle_clipboard)
        self.tab1.layout.addWidget(btn1)

    def change_r(self):
        self.rgb[0] = self.r_level.value()
        self.parent.rgb[0] = self.rgb[0]
        self.update_rgb_hex_percent_label()

    def change_g(self):
        self.rgb[1] = self.g_level.value()
        self.parent.rgb[1] = self.rgb[1]
        self.update_rgb_hex_percent_label()

    def change_b(self):
        self.rgb[2] = self.b_level.value()
        self.parent.rgb[2] = self.rgb[2]
        self.update_rgb_hex_percent_label()

    def x_changed(self):
        self.xy[0] = int(self.line_x.value())
        self.parent.xy[0] = self.xy[0]

    def y_changed(self):
        self.xy[1] = int(self.line_y.value())
        self.parent.xy[1] = self.xy[1]

    def h_changed(self):
        self.hw[0] = int(self.line_height.value())
        self.parent.hw[0] = self.hw[0]

    def w_changed(self):
        self.hw[1] = int(self.line_width.value())
        self.parent.hw[1] = self.hw[1]

    def setRgbClicked(self):
        self.change_r()
        self.change_g()
        self.change_b()

    def setCoordClicked(self):
        self.x_changed()
        self.y_changed()
        self.h_changed()
        self.w_changed()

    def setPercentClicked(self):
        self.change_r()
        self.change_g()
        self.change_b()

    def update_rgb_hex_percent_label(self):
        self.rgb_label.setText(" R: " + str(self.rgb[0]) + " G: " + str(self.rgb[1]) + " B: " + str(self.rgb[2]))
        self.hex_label.setText("HEX: 0x" + self.to_hex_with_zero(self.rgb[0]) + self.to_hex_with_zero(self.rgb[1])
                               + self.to_hex_with_zero(self.rgb[2]))
        self.percent_label.setText("R: "+str(int(self.rgb[0]/256*100))+"%, G:"+str(int(self.rgb[1]/256*100))
                                   +"%, B: "+str(int(self.rgb[2]/256*100))+"%")
        # self.rgb_label.setStyleSheet("QLabel {color : # " + self.to_hex_with_zero(self.rgb[0]) + self.to_hex_with_zero(self.rgb[1])
        #     + self.to_hex_with_zero(self.rgb[2])+"}")

    def to_hex_with_zero(self, dec_num):
        if dec_num == 0:
            return "00"
        else:
            return str(hex(dec_num))[2:]
