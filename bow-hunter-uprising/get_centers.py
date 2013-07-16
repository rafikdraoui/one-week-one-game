import cv2

## HSV THRESHOLD RANGES
# NOTE: In an HSV tuple in OpenCV, the values for H goes from 1 to 180 and
# those for S and V from 1 to 256. The following thresholds have been found by
# starting from the chart at `en.wikipedia.org/wiki/Web_colors#HTML_color_name`
# and experimenting.

MIN_RED_THRESHOLD = (160, 128, 128)
MAX_RED_THRESHOLD = (180, 256, 256)

MIN_BLUE_THRESHOLD = (110, 128, 64)
MAX_BLUE_THRESHOLD = (130, 256, 192)

MIN_YELLOW_THRESHOLD = (20, 64, 128)
MAX_YELLOW_THRESHOLD = (40, 256, 256)


# The area of a colored contoured must be at least that large to be considered
MIN_CONTOUR_AREA = 2000


def get_centers_of_roi(im, min_t, max_t):
    """Return a list of pairs (x, y) corresponding to the coordinates of the
    centers of the region of interests.

    The ROIs are those whose pixels have an HSV value between `min_t` and
    `max_t` in the image `im`. `im` should be an opencv RGB image (as returned
    by `cv2.imread`)
    """

    # smooth the image to remove some noise
    smoothed1 = cv2.blur(im, (3, 3))

    # convert from RGB to HSV (easier to detect hues)
    im_hsv = cv2.cvtColor(smoothed1, cv2.COLOR_BGR2HSV)

    # get a binary image where each pixel is white if its HSV value is between
    # `min_t` and `max_t`, or is black otherwise
    im_thresh = cv2.inRange(im_hsv, min_t, max_t)

    # smooth the resulting binary image to remove noise
    smoothed2 = cv2.blur(im_thresh, (3, 3))

    contours, _ = cv2.findContours(
        smoothed2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    result = []
    for contour in contours:
        # if the area of the contour is too small, do not consider it since it
        # can be considered to be noise
        area = cv2.contourArea(contour)
        if area < MIN_CONTOUR_AREA:
            continue

        # compute the center point of the contour using moments
        moments = cv2.moments(contour)
        center_x = int(moments['m10'] / moments['m00'])
        center_y = int(moments['m01'] / moments['m00'])

        result.append((center_x, center_y))

    return result


def main():
    """Draw a yellow circle centered on the mass centers on each red region of
    the image.
    """
    import sys
    if len(sys.argv) < 3:
        print('Usage: python get_centers.py <input filename> <output filename>')
        sys.exit(1)

    infile, outfile = sys.argv[1:3]

    im = cv2.imread(infile)

    min_t = MIN_RED_THRESHOLD
    max_t = MAX_RED_THRESHOLD
    centers = get_centers_of_roi(im, min_t, max_t)

    radius = 30
    color = (0, 186, 255)  # yellow
    for center in centers:
        cv2.circle(im, center, radius, color)

    cv2.imwrite(outfile, im)


if __name__ == '__main__':
    main()
