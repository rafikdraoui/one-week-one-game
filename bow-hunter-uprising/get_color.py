#!/usr/bin/env python

import cv2
import numpy

numpy.set_printoptions(threshold=numpy.nan)


def get_color(filename):
    """Helper to find color threshold for an image.

    This will output the HSV values of the pixel in the middle row of the input
    image. For best results, use a close-up image of the object you are trying
    to find the color of.
    """
    im = cv2.imread(filename)
    im = cv2.blur(im, (13, 13))
    im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    row = im[len(im)/2]
    print(row)


if __name__ == '__main__':
    import sys
    get_color(sys.argv[1])
