#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap
import time
import json
# import qdarkgraystyle

from MainWindow import MainWindow

if __name__ == "__main__":
    settings = open("./default/userDefault.json")
    settings_text = ''
    for line in settings:
        settings_text += line
    settings.close()
    settings_dict = json.loads(settings_text)
    app = QApplication([])
    # if settings_dict['dark-mode'] == 'true':
    #     app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    sleep_time = len(settings_dict["open-windows"]) * 0.1
    if settings_dict['show-splash'] == 'true':
        for i in range(5):
            splash = QSplashScreen()
            splash.setPixmap(QPixmap('./Icons/loading_' + str(i) + '.png'))
            splash.show()
            time.sleep(sleep_time)
            splash.hide()
    window = MainWindow()
    window.show()
    app.exec_()
