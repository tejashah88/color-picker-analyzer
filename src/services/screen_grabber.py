from PIL import Image, ImageGrab

from src.models.color_pixel_group import ColorPixel

class ScreenGrabber:
    def __init__(self):
        pass


    def grab_color_pixel(self, x, y):
        img = ImageGrab.grab(bbox=(x, y, x + 1, y + 1))

        img_rgb = img.convert(mode='RGB').getpixel((0, 0))
        img_hsv = img.convert(mode='HSV').getpixel((0, 0))
        img_lab = img.convert(mode='LAB').getpixel((0, 0))

        return ColorPixel(
            POS=[x, y],
            RGB=img_rgb,
            HSV=img_hsv,
            LAB=img_lab,
        )
