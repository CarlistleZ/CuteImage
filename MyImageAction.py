from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMainWindow, QMenu

from ClickHandler import ClickHandler


class MyImageAction(QAction):

    def __init__(self, main_window: QMainWindow, message_text: str, container_menu: QMenu,
                 handler: ClickHandler, shortcut: str = "", icon_name: str = ""):
        QAction.__init__(self, message_text, main_window)
        container_menu.addAction(self)
        main_window.toolbar.addAction(self)
        if icon_name != "":
            self.setIcon(QIcon("Icons/" + icon_name))
        self.triggered.connect(handler)
        if shortcut != "":
            self.setShortcut(shortcut)
