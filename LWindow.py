#!/usr/bin/python
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QListView


# Left window in the main window
class LWindow(QFrame):
    def __init__(self, parent):
        QFrame.__init__(self, parent)
        self.parent = parent;
        self.initUI()

    def initUI(self):
        self.rootVbox = QVBoxLayout()

        self.library_lbl = QLabel("Library:")
        self.rootVbox.addWidget(self.library_lbl)
        self.rootVbox.setSpacing(2)
        self.rootVbox.setAlignment(Qt.AlignTop)
        self.add_buttons()

        self.project_file_lbl = QLabel("Project files:")
        self.rootVbox.addWidget(self.project_file_lbl)
        self.init_list()

        self.setLayout(self.rootVbox)

    def add_buttons(self):
        all = self.init_push_button("All")
        all.clicked.connect(self.open_all_clicked)
        self.rootVbox.addWidget(all)

        photos_button = self.init_push_button("Photos")
        photos_button.clicked.connect(self.open_photos_clicked)
        self.rootVbox.addWidget(photos_button)

        memories = self.init_push_button("Memories")
        memories.clicked.connect(self.open_memories_clicked)
        self.rootVbox.addWidget(memories)

        all_events = self.init_push_button("All_events")
        all_events.clicked.connect(self.open_all_events_clicked)
        self.rootVbox.addWidget(all_events)

        imports = self.init_push_button("Imports")
        imports.clicked.connect(self.open_imports_clicked)
        self.rootVbox.addWidget(imports)

    def init_push_button(self, name):
        push_button = QPushButton(name)
        push_button.setIcon(QIcon("Icons/"+name+".png"))
        push_button.setStyleSheet("Text-align:left")
        return push_button

    def open_all_clicked(self):
        self.parent.handler.handle_open()

    def open_photos_clicked(self):
        self.parent.handler.openWithPath("Photos")

    def open_memories_clicked(self):
        self.parent.handler.openWithPath("Memories")

    def open_all_events_clicked(self):
        self.parent.handler.openWithPath("All_events")

    def open_imports_clicked(self):
        self.parent.handler.openWithPath("Imports")

    def init_list(self):
        self.image_list = QListView()
        self.model = QStandardItemModel(self.image_list)
        self.image_list.setIconSize(QSize(60, 60))
        self.image_list.setModel(self.model)
        self.rootVbox.addWidget(self.image_list)
        self.image_list.show()

    def add_list_item(self, file_name):
        short_name = file_name.split("/")[-1]
        short_name.replace(".", "@1x.")
        self.generate_icon(file_name)
        icon_name = "./thumbnails/" + short_name
        item1 = QStandardItem()
        item1.setText(short_name)
        item1.setIcon(QIcon(icon_name))
        self.model.appendRow(item1)

    def generate_icon(self, file_name):
        # TODO
        pass
