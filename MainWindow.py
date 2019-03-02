#!/usr/bin/python
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QToolBar, QMenu, QAction
from IWindow import IWindow
from LWindow import LWindow
from MyImageAction import MyImageAction
from RWindow import RWindow
from BWindow import BWindow
from ClickHandler import ClickHandler


class MainWindow(QMainWindow):

    # initialize the main window
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.init_ui()
        self.show()
        self.handler.handle_open_for_test()

    def init_ui(self):
        self.setWindowTitle("Cute Image Editor")
        self.central_widget = QWidget()
        self.gridLayout = QGridLayout()
        self.central_widget.setLayout(self.gridLayout)
        self.setCentralWidget(self.central_widget)
        self.resize(1280, 768)

        # Add the click handler
        self.handler = ClickHandler(self)

        # Main editing area
        self.mdiArea = IWindow(self)
        # Left window
        self.lwindow = LWindow(self)
        # Right window
        self.rwindow = RWindow(self)
        # Bottom window
        self.bwindow = BWindow(self)

        # Add components to the main grid layout
        self.init_grid()

        self.init_tool_bar()
        self.init_menu_bar()

    def init_grid(self):
        self.gridLayout.setSpacing(2)
        self.gridLayout.addWidget(self.lwindow, 1, 1)
        self.gridLayout.addWidget(self.mdiArea, 1, 2)
        self.gridLayout.addWidget(self.rwindow, 1, 3)
        self.gridLayout.addWidget(self.bwindow, 2, 1, 1, 3)
        self.gridLayout.setColumnMinimumWidth(1, 220)
        self.gridLayout.setColumnMinimumWidth(2, 900)
        self.gridLayout.setColumnMinimumWidth(3, 220)
        self.gridLayout.setRowMinimumHeight(1, 500)
        self.gridLayout.setRowMinimumHeight(2, 140)

    def init_tool_bar(self):
        self.toolBar = QToolBar("Shortcuts")
        self.toolBar.addSeparator()
        self.toolBar.setMaximumHeight(30)
        self.toolBar.setMinimumHeight(30)
        self.addToolBar(self.toolBar)

    def init_menu_bar(self):
        # Create menus in the menu bar as following
        # File  Edit  View  Image  Processing  Profile  Window  Help
        self.file_menu = QMenu("&File")
        self.menuBar().addMenu(self.file_menu)
        self.edit_menu = QMenu("&Edit")
        self.menuBar().addMenu(self.edit_menu)
        self.view_menu = QMenu("&View")
        self.menuBar().addMenu(self.view_menu)
        self.image_menu = QMenu("&Image")
        self.menuBar().addMenu(self.image_menu)
        self.processing_menu = QMenu("Processing")
        self.menuBar().addMenu(self.processing_menu)
        self.profile_menu = QMenu("Profile")
        self.menuBar().addMenu(self.profile_menu)
        self.window_menu = QMenu("&Window")
        self.menuBar().addMenu(self.window_menu)
        self.help_menu = QMenu("&Help")
        self.menuBar().addMenu(self.help_menu)

        # Create actions for each menu
        # Actions for File menu
        self.open_action = MyImageAction(self, "&Open...", self.file_menu, self.handler.handle_open, "Ctrl+O", "open.png")
        self.save_action = MyImageAction(self, "&Save...", self.file_menu, self.handler.handle_save, "Ctrl+S", "save_as.png")
        self.info_action = MyImageAction(self, "&Get Info...", self.file_menu, self.handler.handle_info,  "Ctrl+I", "info.png")
        self.quit_action = MyImageAction(self, "&Quit", self.file_menu, self.close, "Ctrl+Q", "quit.png")

        # Actions for Processing menu
        self.original_color_action = MyImageAction(self, "&Original color", self.processing_menu, self.handler.handle_original_color, "", "origin.png")
        self.reverse_action = MyImageAction(self, "&Reverse", self.processing_menu, self.handler.handle_reverse, "", "reverse.png")
        self.to_grayscale_action = MyImageAction(self, "&Black and white", self.processing_menu, self.handler.handle_to_grayscale, "", "to_grayscale.png")
        self.processing_menu.addSeparator()
        self.saturate_red_action = MyImageAction(self, "&Saturate in red", self.processing_menu, self.handler.handle_saturate_red, "", "saturate_red.png")
        self.saturate_green_action = MyImageAction(self, "&Saturate in green", self.processing_menu, self.handler.handle_saturate_green, "", "saturate_green.png")
        self.saturate_blue_action = MyImageAction(self, "&Saturate in blue", self.processing_menu, self.handler.handle_saturate_blue, "", "saturate_blue.png")
        self.processing_menu.addSeparator()
        self.threshold_action = MyImageAction(self, "&Threshold", self.processing_menu, self.handler.handle_threshold, "", "threshold.png")
        self.blur_action = MyImageAction(self, "&Blur", self.processing_menu, self.handler.handle_blur, "", "blur.png")
        self.sharpen_action = MyImageAction(self, "&Sharpen", self.processing_menu, self.handler.handle_sharpen, "", "sharpen.png")
        self.processing_menu.addSeparator()
        self.ccl_action = MyImageAction(self, "&CCL", self.processing_menu, self.handler.handle_ccl, "", "CCL.png")
        self.hsl_action = MyImageAction(self, "&HSL", self.processing_menu, self.handler.handle_hsl, "", "hsl.png")
        self.outline_action = MyImageAction(self, "&Outline detection", self.processing_menu, self.handler.handle_outline, "", "outline.png")
        self.processing_menu.addSeparator()
        self.floyd_action = MyImageAction(self, "&Floyd", self.processing_menu, self.handler.handle_floyd, "", "floyd.png")
        self.rgb_action = MyImageAction(self, "&RGB", self.processing_menu, self.handler.handle_rgb, "", "rgb.png")
        self.crop_action = MyImageAction(self, "&Crop", self.processing_menu, self.handler.handle_crop, "", "crop.png")

        self.search_help_action = QAction("&Search help...", self)
        self.help_menu.addAction(self.search_help_action)
        self.edit_menu.addAction(self.search_help_action)
        self.view_menu.addAction(self.search_help_action)
        self.image_menu.addAction(self.search_help_action)
        self.profile_menu.addAction(self.search_help_action)
        self.window_menu.addAction(self.search_help_action)


