from itertools import product
from PIL import Image, ImageFilter
from PyQt5.QtGui import qRgb

import RgbImageWindow

def open_file(file_name= '/Users/Carlistle/Desktop/red.jpeg'):
    img = Image.open(file_name)
    img.show()
    return img

def save_file(infile):
    try:
        out = infile.filter(ImageFilter.CONTOUR)
        out.save('/Users/Carlistle/Desktop/red_another.jpeg')
    except IOError:
        print("cannot convert", infile)

def show_in_window(image: Image, rgb_image_window: RgbImageWindow):
    data = image.load()
    height = image.height
    width = image.width
    for y, x in product(range(height), range(width)):
        rgb_tuple = data[x, y]
        rgb_tuple = rgb_tuple[:-1]
        rgb_image_window.image.setPixel(x, y, qRgb(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2]))
    rgb_image_window.update_pixmap(rgb_image_window.image)

if __name__ == '__main__':
    image = open_file()
    save_file(image)