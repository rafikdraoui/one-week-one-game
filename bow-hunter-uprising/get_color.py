#!/usr/bin/env python

from pprint import pprint

import cv2
import numpy

numpy.set_printoptions(threshold=numpy.nan)

def get_color(filename):
    """Helper to find color threshold for an image."""

    im = cv2.imread(filename)
    im = cv2.blur(im, (13, 13))
    im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    row = im[len(im)/2]
    pprint(row)


if __name__ == '__main__':
    import sys
    get_color(sys.argv[1])
