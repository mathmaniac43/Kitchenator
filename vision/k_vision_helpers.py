import argparse
import cv2
import imutils
import math
import numpy
import time

from collections import namedtuple

IMAGE_WIDTH = 640
IMAGE_HEIGHT= 480

#IMAGE_WIDTH =  1920/2
#IMAGE_HEIGHT = 1080/2

IMAGE_WINDOW_NAME = "Image"
CONTROL_WINDOW_NAME = "Controls"
CAMERA_SELECTOR_TRACKBAR_NAME = "Choose Camera Index"
CANNY_MIN_TRACKBAR_NAME = "Canny Min"
CANNY_MAX_TRACKBAR_NAME = "Canny Max"

PIXELS_PER_M = None
RED_X_M = None
RED_Y_M = None

COLOR_THRESHOLD = 60
BLUE_THRESHOLD = COLOR_THRESHOLD + 15

g_mouse_x, g_mouse_y = -1, -1
def mouse_callback(event, x, y, flags, param):
    global g_mouse_x, g_mouse_y
    
    if event == cv2.EVENT_MOUSEMOVE:
        g_mouse_x = x
        g_mouse_y = y
        
def mouse_x():
    global g_mouse_x
    return g_mouse_x
    
def mouse_y():
    global g_mouse_y
    return g_mouse_y
    
def camera():
    global g_camera
    return g_camera
        
def trackbar_callback(val):
    pass

g_camera = None
def camera_selector_callback(val):
    global g_camera, IMAGE_WIDTH, IMAGE_HEIGHT
    
    if g_camera != None:
        g_camera.release()
    
    g_camera = cv2.VideoCapture(val)
    g_camera.set(cv2.cv.CV_CAP_PROP_FPS, 2)
    g_camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,  IMAGE_WIDTH)
    g_camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, IMAGE_HEIGHT)

def is_square(points, rect, tol):
    # points is a list of length-1 lists of [x,y]
    # [ [[x0, y0]], [[x1, y1]], ... ]
    # tol is a percentage of the min width/height to use as a threshold for
    # comparing side lengths of the suspected square
    if len(points) == 4:
        w = rect[1][0]
        h = rect[1][1]
        m = min((w, h))
        
        d_diag_a = math.sqrt((points[0][0][0] - points[2][0][0]) ** 2 +
                             (points[0][0][1] - points[2][0][1]) ** 2)
        d_diag_b = math.sqrt((points[1][0][0] - points[3][0][0]) ** 2 +
                             (points[1][0][1] - points[3][0][1]) ** 2)
        
        return (m * tol > abs(w - h) and (m * tol) > (d_diag_a - d_diag_b))
    
    return False

Square = namedtuple('Square', ['x', 'y', 'w', 'h', 'rot', 'col', 'age'])

def find_pair(squares, c1, c2, lengths_between_centers, tol):
    
    # todo: can probably add more checks for ensuring similar size
    # search newest to oldest
    for i in range(len(squares)-1, -1, -1):
        s1 = squares[i]
        if s1.col == c1:
            for j in range(len(squares)-1, -1, -1):
                if i != j:
                    s2 = squares[j]
                    if s2.col == c2:
                        d = math.sqrt((s1.x - s2.x) ** 2 + (s1.y - s2.y) ** 2)
                        m = min((s1.w, s1.h, s2.w, s2.h))
                        target = m * lengths_between_centers
                        delta = m * tol
                        
                        s1_deg = numpy.rad2deg(s1.rot) % 360
                        s2_deg = numpy.rad2deg(s2.rot) % 360

                        y_dist = s2.y - s1.y
                        x_dist = s2.x - s1.x
                        theta = numpy.rad2deg(math.atan2(y_dist, x_dist)) % 360
                        
                        # todo: these degrees are independent of the squares;
                        # the angle between the squares would need to be taken
                        # into account as well
                        
                        angle_tol = 5 # deg
                        if (d >= (target - delta) and d <= (target + delta) and
                            abs(s1.w - m) < m * tol and abs(s1.h - m) < m * tol and
                            abs(s2.w - m) < m * tol and abs(s2.h - m) < m * tol and
                            abs(theta % 90 - s1_deg % 90) <= angle_tol and
                            abs(theta % 90 - s2_deg % 90) <= angle_tol and
                            abs(s1_deg % 90 - s2_deg % 90) <= angle_tol):
                            print('Next')
                            print((theta, s1_deg, s2_deg))
                            print((theta % 90, s1_deg % 90, s2_deg % 90))
                            return (s1, s2)
    
    return (None, None)

# https://stackoverflow.com/questions/36439384/classifying-rgb-values-in-python
def classify_color(rgb_tuple):
    # eg. rgb_tuple = (2,44,300)

    # add as many colors as appropriate here, but for
    # the stated use case you just want to see if your
    # pixel is 'more red' or 'more green'
    colors = {
        "black": (  0,   0,   0),
        "white": (255, 255, 255),
        "red":   (150,   0,   0), #(255,   0,   0),
        "green": (  0, 150,   0), #(  0, 255,   0),
        "blue":  (  0,   0, 150)  #(  0,   0, 255)
    }
    
    manhattan = lambda x,y : abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2])
    distances = {k: manhattan(v, rgb_tuple) for k, v in colors.items()}
    color = min(distances, key=distances.get)
    return color
    
def get_rectangle_for_squares(s1, s2):
    # with zero rotation (theta=0), s1 is to the left of s2
    
    # TL                TR
    #  ------     ------
    # |      |   |      |
    # |  s1  |   |  s2  |
    # |      |   |      |
    #  ------     ------
    # BL                BR
    
    m = min((s1.w, s1.h, s2.w, s2.h))
    d = m / 2; # distance from each square's center to the edges

    y_dist = s2.y - s1.y
    x_dist = s2.x - s1.x
    theta = math.atan2(y_dist, x_dist)
    
    t_l_x = int(round(s1.x + d * ( math.sin(theta) - math.cos(theta))))
    t_l_y = int(round(s1.y + d * (-math.sin(theta) - math.cos(theta))))
    
    b_l_x = int(round(s1.x + d * (-math.sin(theta) - math.cos(theta))))
    b_l_y = int(round(s1.y + d * (-math.sin(theta) + math.cos(theta))))
    
    b_r_x = int(round(s2.x + d * (-math.sin(theta) + math.cos(theta))))
    b_r_y = int(round(s2.y + d * ( math.sin(theta) + math.cos(theta))))
    
    t_r_x = int(round(s2.x + d * ( math.sin(theta) + math.cos(theta))))
    t_r_y = int(round(s2.y + d * ( math.sin(theta) - math.cos(theta))))
    
    rect = numpy.array([ 
        [[t_l_x, t_l_y]],
        [[b_l_x, b_l_y]],
        [[b_r_x, b_r_y]],
        [[t_r_x, t_r_y]]
    ])
    
    return rect
    
    
def setup_gui():
    global CONTROL_WINDOW_NAME
    global CAMERA_SELECTOR_TRACKBAR_NAME
    global CANNY_MIN_TRACKBAR_NAME
    global CANNY_MAX_TRACKBAR_NAME

    cv2.namedWindow(CONTROL_WINDOW_NAME)
    cv2.createTrackbar(CAMERA_SELECTOR_TRACKBAR_NAME, CONTROL_WINDOW_NAME, 1, 3, camera_selector_callback)
    cv2.createTrackbar(CANNY_MIN_TRACKBAR_NAME, CONTROL_WINDOW_NAME, 120, 255, trackbar_callback)
    cv2.createTrackbar(CANNY_MAX_TRACKBAR_NAME, CONTROL_WINDOW_NAME, 180, 255, trackbar_callback)
    
    cv2.namedWindow(IMAGE_WINDOW_NAME)
    cv2.setMouseCallback(IMAGE_WINDOW_NAME, mouse_callback)


    camera_selector_callback(cv2.getTrackbarPos(CAMERA_SELECTOR_TRACKBAR_NAME, CONTROL_WINDOW_NAME)) # default to the first camera value
    time.sleep(2)
