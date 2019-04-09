#!/usr/bin/python
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QTabWidget, QWidget, QPushButton, QSlider, QSpinBox


# Right window in the main window
import MainWindow


class RWindow(QFrame):
    def __init__(self, parent):
        QFrame.__init__(self, parent)
        self.parent = parent
        self.rgb = [0, 0, 0]
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
        self.tab1.layout.setSpacing(7)

        self.init_rgb()
        self.init_coordinates()

        self.tab1.setLayout(self.tab1.layout)

    def init_tab2(self):
        # TODO
        pass

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

        self.set_rgb = QPushButton("Set")
        # self.set_rgb.clicked.connect(self.setRgbClicked)
        self.tab1.layout.addWidget(self.set_rgb)

    def init_coordinates(self):
        self.tab1.layout.addWidget(QLabel(" "))
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

    def change_r(self):
        self.rgb[0] = self.r_level.value()
        self.parent.rgb[0] = self.rgb[0]

    def change_g(self):
        self.rgb[1] = self.g_level.value()
        self.parent.rgb[1] = self.rgb[1]

    def change_b(self):
        self.rgb[2] = self.b_level.value()
        self.parent.rgb[2] = self.rgb[2]


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
