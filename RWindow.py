#!/usr/bin/python
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QTabWidget, QWidget, QPushButton, QSlider, QSpinBox, \
    QGridLayout, QTextEdit, QDoubleSpinBox

# Right window in the main window
import MainWindow


class RWindow(QFrame):
    def __init__(self, parent):
        QFrame.__init__(self, parent)
        self.parent = parent
        self.rgb = [128, 128, 128]
        self.xy = [0, 0]
        self.hw = [0, 0]
        self.gaussian = 4
        self.mask = [4, 150, 3]
        self.filter_rank = 2
        self.filter_size = 9
        self.kernel_offset = 10
        self.kernel_scale = 10
        self.init_ui()

    def init_ui(self):
        self.rootVbox = QVBoxLayout()
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5= QWidget()
        self.tabs.addTab(self.tab1, "RGB")
        self.tabs.addTab(self.tab2, "Basic")
        self.tabs.addTab(self.tab3, "+")
        self.tabs.addTab(self.tab4, "Pro")
        self.tabs.addTab(self.tab5, "Ker")
        self.tabs.setFixedWidth(220)

        self.init_tab1()
        self.init_tab2()
        self.init_tab3()
        self.init_tab4()
        self.init_tab5()

        self.rootVbox.addWidget(self.tabs)
        self.setLayout(self.rootVbox)



    def indicateClosedWindow(self, window_name):
        self.lbl2.setText(self.lbl2.text() + "\nYou closed "+window_name+" !")

    def init_tab1(self):
        self.tab1.layout = QVBoxLayout(self)
        self.tab1.layout.setAlignment(Qt.AlignTop)
        self.tab1.layout.setSpacing(12)
        self.init_rgb()
        self.tab1.setLayout(self.tab1.layout)

        self.tab1.layout.addWidget(QLabel(" "))
        btn4 = QPushButton('Saturate In Red')
        btn4.setIcon(QIcon('Icons/saturate_red.png'))
        btn4.clicked.connect(self.parent.handler.handle_saturate_red)
        self.tab1.layout.addWidget(btn4)

        btn5 = QPushButton('Saturate In Green')
        btn5.setIcon(QIcon('Icons/saturate_green.png'))
        btn5.clicked.connect(self.parent.handler.handle_saturate_green)
        self.tab1.layout.addWidget(btn5)

        btn6 = QPushButton('Saturate In Blue')
        btn6.setIcon(QIcon('Icons/saturate_blue.png'))
        btn6.clicked.connect(self.parent.handler.handle_saturate_blue)
        self.tab1.layout.addWidget(btn6)

    def init_tab2(self):
        self.tab2.layout = QVBoxLayout(self)
        self.tab2.layout.setAlignment(Qt.AlignTop)
        self.tab2.layout.setSpacing(8)
        self.init_coordinates()
        self.add_basic_tab_buttons()
        self.tab2.setLayout(self.tab2.layout)


    def init_tab3(self):
        self.tab3.layout = QVBoxLayout(self)
        self.tab3.layout.setAlignment(Qt.AlignTop)
        self.tab3.layout.setSpacing(12)
        self.add_more_tab_buttons()
        self.tab3.setLayout(self.tab3.layout)

    def init_tab4(self):
        self.tab4.layout = QVBoxLayout(self)
        self.tab4.layout.setAlignment(Qt.AlignTop)
        self.tab4.layout.setSpacing(12)
        self.add_pro_tab_buttons()
        self.tab4.setLayout(self.tab4.layout)

    def init_tab5(self):
        self.tab5.layout = QVBoxLayout(self)
        self.tab5.layout.setAlignment(Qt.AlignTop)
        self.tab5.layout.setSpacing(4)
        self.add_ker_tab_buttons()
        self.tab5.setLayout(self.tab5.layout)

    def add_basic_tab_buttons(self):

        btn15 = QPushButton('Crop')
        btn15.setIcon(QIcon('Icons/crop.png'))
        btn15.clicked.connect(self.parent.handler.handle_crop)
        self.tab2.layout.addWidget(btn15)


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

        btn4 = QPushButton('Resize')
        btn4.setIcon(QIcon('Icons/resize.png'))
        btn4.clicked.connect(self.parent.handler.handle_resize)

        self.tab2.layout.addWidget(btn4)
        self.tab2.layout.addWidget(QLabel("Height in %: "))
        self.height_percent = QSlider(Qt.Horizontal)
        self.height_percent.setTickPosition(QSlider.TicksBelow)
        self.height_percent.setTickInterval(20)
        self.height_percent.setMinimum(1)
        self.height_percent.setMaximum(100)
        self.height_percent.setValue(100)
        self.tab2.layout.addWidget(self.height_percent)
        self.tab2.layout.addWidget(QLabel("Width in %: "))
        self.width_percent = QSlider(Qt.Horizontal)
        self.width_percent.setTickPosition(QSlider.TicksBelow)
        self.width_percent.setTickInterval(20)
        self.width_percent.setMinimum(1)
        self.width_percent.setMaximum(100)
        self.width_percent.setValue(100)
        self.tab2.layout.addWidget(self.width_percent)

    def add_more_tab_buttons(self):
        btn7 = QPushButton('Smooth')
        btn7.setIcon(QIcon('Icons/smooth.png'))
        btn7.clicked.connect(self.parent.handler.handle_blur)
        self.tab3.layout.addWidget(btn7)

        btn20 = QPushButton('Smooth More')
        btn20.setIcon(QIcon('Icons/smooth.png'))
        btn20.clicked.connect(self.parent.handler.handle_smooth_more)
        self.tab3.layout.addWidget(btn20)

        btn6 = QPushButton('Detail')
        btn6.setIcon(QIcon('Icons/detail.png'))
        btn6.clicked.connect(self.parent.handler.handle_detail)
        self.tab3.layout.addWidget(btn6)

        btn5 = QPushButton('Emboss')
        btn5.setIcon(QIcon('Icons/emboss.png'))
        btn5.clicked.connect(self.parent.handler.handle_emboss)
        self.tab3.layout.addWidget(btn5)

        self.tab3.layout.addWidget(QLabel(" "))

        btn21 = QPushButton('Edge')
        btn21.setIcon(QIcon('Icons/edge.png'))
        btn21.clicked.connect(self.parent.handler.handle_edge)
        self.tab3.layout.addWidget(btn21)

        btn22 = QPushButton('Edge More')
        btn22.setIcon(QIcon('Icons/edge.png'))
        btn22.clicked.connect(self.parent.handler.handle_edge_more)
        self.tab3.layout.addWidget(btn22)

        btn23 = QPushButton('Find Edges')
        btn23.setIcon(QIcon('Icons/find_edges.png'))
        btn23.clicked.connect(self.parent.handler.handle_find_edges)
        self.tab3.layout.addWidget(btn23)

        self.tab3.layout.addWidget(QLabel(" "))

        btn8 = QPushButton('Blur')
        btn8.setIcon(QIcon('Icons/blur.png'))
        btn8.clicked.connect(self.parent.handler.handle_blur)
        self.tab3.layout.addWidget(btn8)

        btn24 = QPushButton('Gaussian Blur')
        btn24.setIcon(QIcon('Icons/gaussian.png'))
        btn24.clicked.connect(self.parent.handler.handle_gaussian_blur)
        self.tab3.layout.addWidget(btn24)

        btn25 = QPushButton('Box Blur')
        btn25.setIcon(QIcon('Icons/box.png'))
        btn25.clicked.connect(self.parent.handler.handle_box_blur)
        self.tab3.layout.addWidget(btn25)

        self.tab3.layout.addWidget(QLabel("Radius:"))
        self.gaussian_level = QSlider(Qt.Horizontal)
        self.gaussian_level.setTickPosition(QSlider.TicksBelow)
        self.gaussian_level.setTickInterval(1)
        self.gaussian_level.setMinimum(1)
        self.gaussian_level.setMaximum(8)
        self.gaussian_level.setValue(4)
        self.tab3.layout.addWidget(self.gaussian_level)
        self.gaussian_level.valueChanged.connect(self.change_gaussian)

        btn9 = QPushButton('Sharpen')
        btn9.setIcon(QIcon('Icons/sharpen.png'))
        btn9.clicked.connect(self.parent.handler.handle_sharpen)
        self.tab3.layout.addWidget(btn9)

        btn12 = QPushButton('Outline Detection')
        btn12.setIcon(QIcon('Icons/outline.png'))
        btn12.clicked.connect(self.parent.handler.handle_outline)
        self.tab3.layout.addWidget(btn12)

        btn17 = QPushButton('Dithering')
        btn17.setIcon(QIcon('Icons/floyd.png'))
        btn17.clicked.connect(self.parent.handler.handle_dithering)
        self.tab3.layout.addWidget(btn17)

    def add_pro_tab_buttons(self):
        btn1 = QPushButton('Unsharp Mask')
        btn1.setIcon(QIcon('Icons/mask.png'))
        btn1.clicked.connect(self.parent.handler.handle_unsharp_mask)
        self.tab4.layout.addWidget(btn1)

        self.tab4.layout.addWidget(QLabel("Radius:"))
        self.mask_r_level = QSlider(Qt.Horizontal)
        self.mask_r_level.setTickPosition(QSlider.TicksBelow)
        self.mask_r_level.setTickInterval(1)
        self.mask_r_level.setMinimum(1)
        self.mask_r_level.setMaximum(8)
        self.mask_r_level.setValue(4)
        self.tab4.layout.addWidget(self.mask_r_level)
        self.mask_r_level.valueChanged.connect(self.change_mask_r)

        self.tab4.layout.addWidget(QLabel("Percent:"))
        self.mask_p_level = QSlider(Qt.Horizontal)
        self.mask_p_level.setTickPosition(QSlider.TicksBelow)
        self.mask_p_level.setTickInterval(50)
        self.mask_p_level.setMinimum(1)
        self.mask_p_level.setMaximum(300)
        self.mask_p_level.setValue(150)
        self.tab4.layout.addWidget(self.mask_p_level)
        self.mask_p_level.valueChanged.connect(self.change_mask_p)

        self.tab4.layout.addWidget(QLabel("Threshold:"))
        self.mask_t_level = QSlider(Qt.Horizontal)
        self.mask_t_level.setTickPosition(QSlider.TicksBelow)
        self.mask_t_level.setTickInterval(1)
        self.mask_t_level.setMinimum(1)
        self.mask_t_level.setMaximum(6)
        self.mask_t_level.setValue(3)
        self.tab4.layout.addWidget(self.mask_t_level)
        self.mask_t_level.valueChanged.connect(self.change_mask_t)

        btn2 = QPushButton('Min Filter')
        btn2.setIcon(QIcon('Icons/filter-512.png'))
        btn2.clicked.connect(self.parent.handler.handle_min_filter)
        self.tab4.layout.addWidget(btn2)

        btn3 = QPushButton('Max Filter')
        btn3.setIcon(QIcon('Icons/filter-512.png'))
        btn3.clicked.connect(self.parent.handler.handle_max_filter)
        self.tab4.layout.addWidget(btn3)

        btn4 = QPushButton('Median Filter')
        btn4.setIcon(QIcon('Icons/filter-512.png'))
        btn4.clicked.connect(self.parent.handler.handle_median_filter)
        self.tab4.layout.addWidget(btn4)

        btn5 = QPushButton('Rank Filter')
        btn5.setIcon(QIcon('Icons/filter-512.png'))
        btn5.clicked.connect(self.parent.handler.handle_min_filter)
        self.tab4.layout.addWidget(btn5)

        self.tab4.layout.addWidget(QLabel("Rank:"))
        self.rank_level = QSlider(Qt.Horizontal)
        self.rank_level.setTickPosition(QSlider.TicksBelow)
        self.rank_level.setTickInterval(1)
        self.rank_level.setMinimum(1)
        self.rank_level.setMaximum(5)
        self.rank_level.setValue(2)
        self.tab4.layout.addWidget(self.rank_level)
        self.rank_level.valueChanged.connect(self.change_rank)

        self.tab4.layout.addWidget(QLabel("Size:"))
        self.size_level = QSlider(Qt.Horizontal)
        self.size_level.setTickPosition(QSlider.TicksBelow)
        self.size_level.setTickInterval(4)
        self.size_level.setMinimum(1)
        self.size_level.setMaximum(18)
        self.size_level.setValue(9)
        self.tab4.layout.addWidget(self.size_level)
        self.size_level.valueChanged.connect(self.change_size)

        btn16 = QPushButton('Timer')
        btn16.setIcon(QIcon('Icons/timer.png'))
        btn16.clicked.connect(self.parent.handler.handle_timer)
        self.tab4.layout.addWidget(btn16)

        btn10 = QPushButton('Object Labeling')
        btn10.setIcon(QIcon('Icons/CCL.png'))
        btn10.clicked.connect(self.parent.handler.handle_ccl)
        self.tab4.layout.addWidget(btn10)

    def add_ker_tab_buttons(self):
        self.tab5.layout.addWidget(QLabel("Kernel (3 * 3):"))

        btn16 = QPushButton('Kernel')
        btn16.setIcon(QIcon('Icons/kernel.png'))
        btn16.clicked.connect(self.parent.handler.handle_kernel)
        self.tab5.layout.addWidget(btn16)

        self.scale_lable = QLabel("Scale: 1.0")
        self.tab5.layout.addWidget(self.scale_lable)
        self.kernel_scale_level = QSlider(Qt.Horizontal)
        self.kernel_scale_level.setTickPosition(QSlider.TicksBelow)
        self.kernel_scale_level.setTickInterval(5)
        self.kernel_scale_level.setMinimum(0)
        self.kernel_scale_level.setMaximum(20)
        self.kernel_scale_level.setValue(10)
        self.tab5.layout.addWidget(self.kernel_scale_level)
        self.kernel_scale_level.valueChanged.connect(self.change_kerkel_scale)

        self.offset_label = QLabel("Offset: 0.0")
        self.tab5.layout.addWidget(self.offset_label)
        self.kernel_offset_level = QSlider(Qt.Horizontal)
        self.kernel_offset_level.setTickPosition(QSlider.TicksBelow)
        self.kernel_offset_level.setTickInterval(5)
        self.kernel_offset_level.setMinimum(0)
        self.kernel_offset_level.setMaximum(20)
        self.kernel_offset_level.setValue(10)
        self.tab5.layout.addWidget(self.kernel_offset_level)
        self.kernel_offset_level.valueChanged.connect(self.change_kerkel_offset)

        self.grid = QGridLayout()
        self.grid.setSpacing(8)
        self.grid.setAlignment(Qt.AlignTop)
        frame = QFrame()
        frame.setLayout(self.grid)
        self.tab5.layout.addWidget(frame)

        self.idx11 = QDoubleSpinBox()
        self.grid.addWidget(self.idx11, 1, 1, Qt.AlignLeading)
        self.idx12 = QDoubleSpinBox()
        self.grid.addWidget(self.idx12, 1, 2, Qt.AlignLeading)
        self.idx13 = QDoubleSpinBox()
        self.grid.addWidget(self.idx13, 1, 3, Qt.AlignLeading)
        self.idx21 = QDoubleSpinBox()
        self.grid.addWidget(self.idx21, 2, 1, Qt.AlignLeading)
        self.idx22 = QDoubleSpinBox()
        self.grid.addWidget(self.idx22, 2, 2, Qt.AlignLeading)
        self.idx23 = QDoubleSpinBox()
        self.grid.addWidget(self.idx23, 2, 3, Qt.AlignLeading)
        self.idx31 = QDoubleSpinBox()
        self.grid.addWidget(self.idx31, 3, 1, Qt.AlignLeading)
        self.idx32 = QDoubleSpinBox()
        self.grid.addWidget(self.idx32, 3, 2, Qt.AlignLeading)
        self.idx33 = QDoubleSpinBox()
        self.grid.addWidget(self.idx33, 3, 3, Qt.AlignLeading)

        self.idx_fields = [self.idx11, self.idx12, self.idx13,
                      self.idx21, self.idx22, self.idx23,
                      self.idx31, self.idx32, self.idx33]
        for idx in self.idx_fields:
            idx.setFixedWidth(50)
            idx.setFixedHeight(25)
            idx.setValue(0)
            idx.setMinimum(0 - 8.0)
            idx.setMaximum(8.0)

        self.tab5.layout.addWidget(QLabel(" "))
        btn13 = QPushButton('Custom Filter')
        btn13.setIcon(QIcon('Icons/filter.png'))
        btn13.clicked.connect(self.parent.handler.handle_custom_filter)
        self.tab5.layout.addWidget(btn13)

        self.rgb_grid = QGridLayout()
        self.rgb_grid.setSpacing(3)
        self.rgb_grid.setAlignment(Qt.AlignTop)
        rgb_frame = QFrame()
        rgb_frame.setLayout(self.rgb_grid)
        self.tab5.layout.addWidget(rgb_frame)

        self.rgb_input = []
        self.rgb_grid.addWidget(QLabel("Red transformation:"), 0, 0, 1, 3)
        r1 = QDoubleSpinBox()
        r1.setMinimum(-255)
        r1.setMaximum(255)
        r1.setValue(1.0)
        self.rgb_input.append(r1)
        self.rgb_grid.addWidget(r1, 1, 0)
        self.rgb_grid.addWidget(QLabel(" * R + "), 1, 1)
        r2 = QDoubleSpinBox()
        r2.setMinimum(-255)
        r2.setMaximum(255)
        self.rgb_input.append(r2)
        self.rgb_grid.addWidget(r2, 1, 2)
        self.rgb_grid.addWidget(QLabel("Green transformation:"), 2, 0, 1, 3)
        g1 = QDoubleSpinBox()
        g1.setMinimum(-255)
        g1.setMaximum(255)
        g1.setValue(1.0)
        self.rgb_input.append(g1)
        self.rgb_grid.addWidget(g1, 3, 0)
        self.rgb_grid.addWidget(QLabel(" * G + "), 3, 1)
        g2 = QDoubleSpinBox()
        g2.setMinimum(-255)
        g2.setMaximum(255)
        self.rgb_input.append(g2)
        self.rgb_grid.addWidget(g2, 3, 2)
        self.rgb_grid.addWidget(QLabel("Blue transformation:"), 4, 0, 1, 3)
        b1 = QDoubleSpinBox()
        b1.setMinimum(-255)
        b1.setMaximum(255)
        b1.setValue(1.0)
        self.rgb_input.append(b1)
        self.rgb_grid.addWidget(b1, 5, 0)
        self.rgb_grid.addWidget(QLabel(" * B + "), 5, 1)
        b2 = QDoubleSpinBox()
        self.rgb_input.append(b2)
        b2.setMinimum(-255)
        b2.setMaximum(255)
        self.rgb_grid.addWidget(b2, 5, 2)

    def init_rgb(self):
        self.r_level_label = QLabel("Red Level: 128")
        self.tab1.layout.addWidget(self.r_level_label)
        self.r_level = QSlider(Qt.Horizontal)
        self.r_level.setTickPosition(QSlider.TicksBelow)
        self.r_level.setTickInterval(64)
        self.r_level.setMinimum(0)
        self.r_level.setMaximum(255)
        self.r_level.setValue(128)
        self.tab1.layout.addWidget(self.r_level)
        self.r_level.valueChanged.connect(self.change_r)

        self.g_level_label = QLabel("Green Level: 128")
        self.tab1.layout.addWidget(self.g_level_label)
        self.g_level = QSlider(Qt.Horizontal)
        self.g_level.setTickPosition(QSlider.TicksBelow)
        self.g_level.setTickInterval(64)
        self.g_level.setMinimum(0)
        self.g_level.setMaximum(255)
        self.g_level.setValue(128)
        self.tab1.layout.addWidget(self.g_level)
        self.g_level.valueChanged.connect(self.change_g)

        self.b_level_label = QLabel("Blue Level: 128")
        self.tab1.layout.addWidget(self.b_level_label)
        self.b_level = QSlider(Qt.Horizontal)
        self.b_level.setTickPosition(QSlider.TicksBelow)
        self.b_level.setTickInterval(64)
        self.b_level.setMinimum(0)
        self.b_level.setMaximum(255)
        self.b_level.setValue(128)
        self.tab1.layout.addWidget(self.b_level)
        self.b_level.valueChanged.connect(self.change_b)

        btn14 = QPushButton('RGB')
        btn14.setIcon(QIcon('Icons/rgb.png'))
        btn14.clicked.connect(self.parent.handler.handle_rgb)
        self.tab1.layout.addWidget(btn14)

        btn7 = QPushButton('Threshold')
        btn7.setIcon(QIcon('Icons/threshold.png'))
        btn7.clicked.connect(self.parent.handler.handle_threshold)
        self.tab1.layout.addWidget(btn7)

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
        x_label = QLabel("X Value:")
        self.tab2.layout.addWidget(x_label)
        self.line_x = QSpinBox()
        self.line_x.setMinimum(0)
        self.line_x.setMaximum(1000)
        self.line_x.setValue(0)
        self.line_x.setSingleStep(10)
        self.line_x.valueChanged.connect(self.x_changed)
        self.tab2.layout.addWidget(self.line_x)

        y_label = QLabel("Y Value:")
        self.tab2.layout.addWidget(y_label)
        self.line_y = QSpinBox()
        self.line_y.setMinimum(0)
        self.line_y.setMaximum(1000)
        self.line_y.setValue(0)
        self.line_y.setSingleStep(10)
        self.line_y.valueChanged.connect(self.y_changed)
        self.tab2.layout.addWidget(self.line_y)

        height_label = QLabel("Width:")
        self.tab2.layout.addWidget(height_label)
        self.line_height = QSpinBox()
        self.line_height.setMinimum(0)
        self.line_height.setMaximum(1000)
        self.line_height.setValue(200)
        self.line_height.setSingleStep(10)
        self.line_height.valueChanged.connect(self.h_changed)
        self.tab2.layout.addWidget(self.line_height)

        width_label = QLabel("Height:")
        self.tab2.layout.addWidget(width_label)
        self.line_width = QSpinBox()
        self.line_width.setMinimum(0)
        self.line_width.setMaximum(1000)
        self.line_width.setValue(200)
        self.line_width.setSingleStep(10)
        self.line_width.valueChanged.connect(self.w_changed)
        self.tab2.layout.addWidget(self.line_width)

        self.set_coord = QPushButton("Set Dimensions")
        self.set_coord.clicked.connect(self.setCoordClicked)
        self.tab2.layout.addWidget(self.set_coord)

        btn1 = QPushButton('Clipboard')
        btn1.setIcon(QIcon('Icons/clipboard.png'))
        btn1.clicked.connect(self.parent.handler.handle_clipboard)
        self.tab2.layout.addWidget(btn1)
        self.tab2.layout.addWidget(QLabel(" "))

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

    def change_gaussian(self):
        self.gaussian = int(self.gaussian_level.value())

    def change_mask_r(self):
        self.mask[0] = int(self.mask_r_level.value())

    def change_mask_p(self):
        self.mask[1] = int(self.mask_p_level.value())

    def change_mask_t(self):
        self.mask[2] = int(self.mask_t_level.value())

    def change_rank(self):
        self.filter_rank = int(self.rank_level.value())

    def change_size(self):
        self.filter_size = int(self.size_level.value())

    def change_kerkel_offset(self):
        self.kernel_offset = int(self.kernel_offset_level.value())
        self.offset_label.setText("Offset: " + str(self.kernel_offset_level.value() / 10 - 1.0))


    def change_kerkel_scale(self):
        self.kernel_scale = int(self.kernel_scale_level.value())
        self.scale_lable.setText("Scale: " + str(self.kernel_scale_level.value() / 10))

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
        self.r_level_label.setText("Red Level: " + str(self.rgb[0]))
        self.g_level_label.setText("Green Level: " + str(self.rgb[1]))
        self.b_level_label.setText("Blue Level: " + str(self.rgb[2]))
        self.rgb_label.setText(" RGB: " + str(self.rgb[0]) + ", " + str(self.rgb[1]) + ", " + str(self.rgb[2]))
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
