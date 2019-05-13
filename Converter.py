from itertools import product
from PIL import Image, ImageFilter
from PyQt5.QtGui import qRgb
from PyQt5.QtWidgets import QSizePolicy

import RgbImageWindow

def open_file(file_name= '/Users/Carlistle/Developer/PyCharmWorkspace/CuteImage/Photos_Library_photoslibrary/red_small.jpeg'):
    img = Image.open(file_name)
    img.show()
    return img

def save_file(infile):
    try:
        out = infile.filter(ImageFilter.CONTOUR)
        out.save('/Users/Carlistle/Desktop/red_another.jpeg')
    except IOError:
        print("cannot convert", infile)


# Displays a PIL image in an rgb_image_window
def show_in_window(image: Image, rgb_image_window: RgbImageWindow):
    data = image.load()
    height = image.height
    width = image.width
    image.show()
    for y, x in product(range(1, height), range(1, width)):
        rgb_tuple = data[x, y]
        if len(rgb_tuple) == 4:
            rgb_tuple = rgb_tuple[:-1]
        rgb_image_window.image.setPixel(x, y, qRgb(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2]))
    # rgb_image_window.update_pixmap(rgb_image_window.image)
    # rgb_image_window.setWidget(rgb_image_window.image_label)
    rgb_image_window.resize(rgb_image_window.pixmap.size())
    rgb_image_window.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)