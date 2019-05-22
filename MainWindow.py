#!/usr/bin/python
import json

from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QToolBar, QMenu, QAction, QApplication
from IWindow import IWindow
from LWindow import LWindow
from MyImageAction import MyImageAction
from RWindow import RWindow
from BWindow import BWindow
from ClickHandler import ClickHandler


class MainWindow(QMainWindow):

    # initialize the main window
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.init_ui()
        self.show()
        self.rgb = [128, 128, 128]
        self.xy = [0, 0]
        self.hw = [0, 0]
        self.filter = 1
        self.handler.handle_open_for_json()
        QApplication.clipboard().dataChanged.connect(self.clipboardChanged)
        self.clipboardChanged()

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
        # Left window~
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

        self.toolbar = QToolBar("Shortcuts")
        self.addToolBar(self.toolbar)
        # action_list = [[self.open_action, self.save_action, self.info_action, self.quit_action, self.search_help_action],
        #                [self.original_color_action, self.reverse_action, self.to_grayscale_action, self],
        #                [self.saturate_red_action, self.saturate_blue_action, self.saturate_green_action],
        #                [self.threshold_action, self.blur_action, self.sharpen_action],
        #                [self.ccl_action, self.hsl_action, self.outline_action],
        #                [self.floyd_action, self.rgb_action, self.crop_action]]
        # for sublist in action_list:
        #     for action in sublist:
        #         self.toolbar.addAction(QAction(action))
        #     self.toolbar.addSeparator()
        self.toolbar.setMaximumHeight(30)
        self.toolbar.setMinimumHeight(30)

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
        self.share_menu = QMenu("Share")
        self.menuBar().addMenu(self.share_menu)
        self.window_menu = QMenu("&Window")
        self.menuBar().addMenu(self.window_menu)
        self.help_menu = QMenu("&Help")
        self.menuBar().addMenu(self.help_menu)

        # Create actions for each menu
        # Actions for File menu
        self.open_action = MyImageAction(self, "&Open...", self.file_menu, self.handler.handle_open, "Ctrl+O", "open.png")
        self.save_action = MyImageAction(self, "&Save...", self.file_menu, self.handler.handle_save, "Ctrl+S", "save_as.png")
        self.info_action = MyImageAction(self, "&Get Info...", self.file_menu, self.handler.handle_info,  "Ctrl+I", "info.png")
        self.camera_action = MyImageAction(self, "&Camera", self.edit_menu, self.handler.handle_camera,  "", "camera.png")
        self.url_action = MyImageAction(self, "&Open URL", self.edit_menu, self.handler.handle_url,  "", "url.png")
        self.clipboard_action = MyImageAction(self, "&Copy To Clipboard", self.edit_menu, self.handler.handle_clipboard,  "", "clipboard.png")
        self.show_folder_action = MyImageAction(self, "&Show In Finder", self.file_menu, self.handler.handle_finder, "Ctrl+F", "finder.png")
        self.open_with_app_action = MyImageAction(self, "&Open With App", self.file_menu, self.handler.handle_open_with_app,  "", "app.png")
        self.instagram_action = MyImageAction(self, "&Share In Instagram", self.share_menu,
                                                  self.handler.handle_instagram, "", "instagram.png")
        self.twitter_action = MyImageAction(self, "&Share In Twitter", self.share_menu,
                                              self.handler.handle_twitter, "", "twitter.png")
        self.snapchat_action = MyImageAction(self, "&Share In Snapchat", self.share_menu,
                                              self.handler.handle_snapchat, "", "snapchat.png")
        # Actions for Processing menu
        self.original_color_action = MyImageAction(self, "&Original color", self.image_menu, self.handler.handle_original_color, "", "origin.png")
        self.reverse_action = MyImageAction(self, "&Reverse", self.image_menu, self.handler.handle_reverse, "", "reverse.png")
        self.to_grayscale_action = MyImageAction(self, "&Black and white", self.image_menu, self.handler.handle_to_grayscale, "", "to_grayscale.png")
        self.image_menu.addSeparator()
        self.saturate_red_action = MyImageAction(self, "&Saturate in red", self.image_menu, self.handler.handle_saturate_red, "", "saturate_red.png")
        self.saturate_green_action = MyImageAction(self, "&Saturate in green", self.image_menu, self.handler.handle_saturate_green, "", "saturate_green.png")
        self.saturate_blue_action = MyImageAction(self, "&Saturate in blue", self.image_menu, self.handler.handle_saturate_blue, "", "saturate_blue.png")

        self.threshold_action = MyImageAction(self, "&Threshold", self.processing_menu, self.handler.handle_threshold, "", "threshold.png")

        self.blur_action = MyImageAction(self, "&Blur", self.processing_menu, self.handler.handle_blur, "", "blur.png")
        self.gaussian_blur_action = MyImageAction(self, "&Gaussian Blur", self.processing_menu, self.handler.handle_gaussian_blur, "", "gaussian.png")
        self.box_blur_action = MyImageAction(self, "&Box Blur", self.processing_menu, self.handler.handle_box_blur, "", "box.png")
        self.sharpen_action = MyImageAction(self, "&Sharpen", self.processing_menu, self.handler.handle_sharpen, "", "sharpen.png")
        self.processing_menu.addSeparator()
        self.filter_action = MyImageAction(self, "&Filter", self.processing_menu, self.handler.handle_filter,
                                              "", "filter.png")
        self.ccl_action = MyImageAction(self, "&CCL", self.processing_menu, self.handler.handle_ccl, "", "CCL.png")
        # self.hsl_action = MyImageAction(self, "&HSL", self.processing_menu, self.handler.handle_hsl, "", "hsl.png")
        self.outline_action = MyImageAction(self, "&Outline detection", self.processing_menu, self.handler.handle_outline, "", "outline.png")
        self.smooth_action = MyImageAction(self, "&Smooth", self.processing_menu, self.handler.handle_smooth, "", "smooth.png")
        self.smooth_more_action = MyImageAction(self, "&Smooth More", self.processing_menu, self.handler.handle_smooth_more, "", "smooth.png")
        self.detail_action = MyImageAction(self, "&Detail", self.processing_menu, self.handler.handle_detail, "", "detail.png")
        self.emboss_action = MyImageAction(self, "&Emboss", self.processing_menu, self.handler.handle_emboss, "", "emboss.png")
        self.edge_action = MyImageAction(self, "&Edge", self.processing_menu, self.handler.handle_edge, "", "edge.png")
        self.edge_more_action = MyImageAction(self, "&Edge More", self.processing_menu, self.handler.handle_edge_more, "", "edge.png")
        self.find_edges_action = MyImageAction(self, "&Find Edges", self.processing_menu, self.handler.handle_find_edges, "", "find_edges.png")

        self.processing_menu.addSeparator()
        self.min_filter_action = MyImageAction(self, "&Min Filter", self.processing_menu, self.handler.handle_min_filter, "", "filter-512.png")
        self.max_filter_action = MyImageAction(self, "&Max Filter", self.processing_menu, self.handler.handle_max_filter, "", "filter-512.png")
        self.median_filter_action = MyImageAction(self, "&Median Filter", self.processing_menu, self.handler.handle_median_filter, "", "filter-512.png")
        self.rank_filter_action = MyImageAction(self, "&Rank Filter", self.processing_menu, self.handler.handle_rank_filter, "", "filter-512.png")

        self.processing_menu.addSeparator()
        self.floyd_action = MyImageAction(self, "&Dithering", self.processing_menu, self.handler.handle_dithering, "", "floyd.png")
        self.rgb_action = MyImageAction(self, "&RGB", self.processing_menu, self.handler.handle_rgb, "", "rgb.png")
        self.crop_action = MyImageAction(self, "&Crop", self.processing_menu, self.handler.handle_crop, "", "crop.png")
        self.timer_action = MyImageAction(self, "&Timer", self.processing_menu, self.handler.handle_timer, "", "timer.png")
        self.kernel_action = MyImageAction(self, "&Kernel", self.processing_menu, self.handler.handle_kernel, "", "kernel.png")
        self.view_menu.addSeparator()
        self.toggle_l_action = MyImageAction(self, "&Toggle Left", self.view_menu, self.handler.handle_toggle_l, "Ctrl+1",
                                              "l_window.png")
        self.toggle_r_action = MyImageAction(self, "&Toggle Right", self.view_menu, self.handler.handle_toggle_r, "Ctrl+2",
                                              "r_window.png")
        self.toggle_b_action = MyImageAction(self, "&Toggle Bottom", self.view_menu, self.handler.handle_toggle_b, "Ctrl+0",
                                              "b_window.png")
        self.view_menu.addSeparator()
        self.close_all_action = MyImageAction(self, "&Close All", self.window_menu, self.handler.handle_close_all, "",
                                              "close.png")
        self.quit_action = MyImageAction(self, "&Quit", self.file_menu, self.close, "Ctrl+Q", "quit.png")


        self.search_help_action = QAction("&Search help...", self)
        self.actions = [[self.open_action, self.save_action, self.info_action], [self.camera_action,
                        self.clipboard_action], [self.url_action, self.show_folder_action, self.open_with_app_action],
                        [self.instagram_action, self.twitter_action, self.snapchat_action],
                        [QAction(),QAction(),QAction(),QAction(),QAction(),QAction(),QAction(),QAction(),QAction(),
                         QAction(),QAction(),QAction(),QAction()],
                        [self.toggle_l_action, self.toggle_r_action, self.toggle_b_action],
                        [self.close_all_action, self.quit_action]]
        for sub_list in self.actions:
            for action in sub_list:
                self.toolbar.addAction(action)
            if sub_list != self.actions[-1] and sub_list != self.actions[-3] and sub_list != self.actions[-4]:
                self.toolbar.addSeparator()

        self.help_menu.addAction(self.search_help_action)

    def get_rgb(self):
        return self.rgb

    def get_xy(self):
        return self.xy

    def get_hw(self):
        return self.hw

    def clipboardChanged(self):
        self.clip_board_text = QApplication.clipboard().text()
        self.clip_board_image = QApplication.clipboard().image()

    def set_rgb(self, r=128, g=128, b=128):
        self.rgb = [r, g, b]

    def closeEvent(self, event):
        self.handler.handle_close_event()

