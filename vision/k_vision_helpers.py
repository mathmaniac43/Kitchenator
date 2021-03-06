import argparse
import cv2
import imutils
import json
import math
import numpy
import time

from collections import namedtuple

# Constants
HOME = False

if HOME:
    IMAGE_WIDTH = 640
    IMAGE_HEIGHT= 480
    
    FLIP_VALUE = -1
    
    COLORS = {
        "black": ( 30,  30,  30),
        "orange":(255, 150,  50),
        "green": (100, 160, 100),
        "blue":  ( 20, 110, 200),
        "purple":( 80,  80, 180),
        "white": (255, 255, 255)
    }
    
    DEFAULT_CAMERA = 1
    
else: # LAB

    IMAGE_WIDTH =  1920/2
    IMAGE_HEIGHT = 1080/2
    
    FLIP_VALUE = 1
    
    COLORS = {
        "black": ( 50,  50,  50),
        "orange":(255, 150,  50),
        "green": (180, 255, 110),
        "blue":  ( 15, 115, 190),
        "purple":(120,  90, 220),
        "white": (255, 255, 255)
    }
    
    DEFAULT_CAMERA = 0

IMAGE_WINDOW_NAME = "Image"
CONTROL_WINDOW_NAME = "Controls"
CAMERA_SELECTOR_TRACKBAR_NAME = "Choose Camera Index"
CANNY_MIN_TRACKBAR_NAME = "Canny Min"
CANNY_MAX_TRACKBAR_NAME = "Canny Max"

# Globals

g_mouse_x = -1,
g_mouse_y = -1
g_camera = None

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
        
        return (m * tol > abs(w - h) and (m * tol) > abs(d_diag_a - d_diag_b))
    
    return False

Square = namedtuple('Square', ['x', 'y', 'w', 'h', 'rot', 'col', 'age'])

def find_pair(squares, c1, c2, lengths_between_centers, dist_tol, angle_tol_deg):
    
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
                        delta = m * dist_tol
                        
                        s1_deg = s1.rot % 90 # squares are 4-angle symmetrical
                        s2_deg = s2.rot % 90 # squares are 4-angle symmetrical

                        y_dist = s2.y - s1.y
                        x_dist = s2.x - s1.x
                        theta = numpy.rad2deg(math.atan2(y_dist, x_dist)) % 360
                        
                        if (d >= (target - delta) and d <= (target + delta) and
                            abs(s1.w - m) < delta and abs(s1.h - m) < delta and
                            abs(s2.w - m) < delta and abs(s2.h - m) < delta and
                            abs(theta % 90 - s1_deg) <= angle_tol_deg and
                            abs(theta % 90 - s2_deg) <= angle_tol_deg and
                            abs(s1_deg - s2_deg) <= angle_tol_deg):
                            return (s1, s2)
    
    return (None, None)

# https://stackoverflow.com/questions/36439384/classifying-rgb-values-in-python
def classify_color(rgb_tuple):
    global COLORS
    
    manhattan = lambda x,y : abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2])
    distances = {k: manhattan(v, rgb_tuple) for k, v in COLORS.items()}
    color = min(distances, key=distances.get)
    return color
    
def get_rectangle_for_squares(s1, s2):
    # with zero rotation (theta=0), s1 is to the left of s2
    # rotation goes clockwise
    
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
    
    t_l = apply_transform((s1.x, s1.y), theta, (-d, -d), True)
    b_l = apply_transform((s1.x, s1.y), theta, (-d,  d), True)
    t_r = apply_transform((s2.x, s2.y), theta, ( d, -d), True)
    b_r = apply_transform((s2.x, s2.y), theta, ( d,  d), True)
    
    rect = numpy.array([ 
        [t_l],
        [b_l],
        [b_r],
        [t_r]
    ])
    
    return (rect, theta)

# This works for both pixels AND distances =)
def apply_transform(center, theta, translation, pixel = False):
    x = center[0]
    y = center[1]
    dx = translation[0]
    dy = translation[1]
    
    result = (
        (x + dx * math.cos(theta) - dy * math.sin(theta)),
        (y + dx * math.sin(theta) + dy * math.cos(theta))
    )
    
    if pixel:
        result = (
            int(round(result[0])),
            int(round(result[1]))
        )
    
    return result
    
#
def inverse_transform(center, theta, point, pixel = False):
    new_center = (0, 0)
    new_point = (point[0] - center[0], point[1] - center[1])
    return apply_transform(new_center, -theta, new_point, pixel)

def to_position_json(c, right, down, rot, origin_rot):
    # Assume that origin is at center of robot, with right
    # along the robot's +Y axis and down along the robot's +X axis
    # (Tag to right, green stretched left)
    
    x = -right
    y = down
    
    z = 0
    if c == "purple" or c == "blue":
        z = 0.09 # 9 cm
    if c == "orange":
        z = 0.2 # 20 cm
    
    # zero in line with origin's right axis, clockwise
    zero_rel_rot = rot - origin_rot
    
    # zero in line with origin's right axis, counterclockwise
    neg_zero_rel_rot = -zero_rel_rot
    
    # zero in line with robot's +X axis, counterclockwise
    x_rot = neg_zero_rel_rot + math.pi/2
    if c == "purple":
        x_rot = x_rot + math.pi
    
    while x_rot < -math.pi:
        x_rot = x_rot + 2*math.pi
    while x_rot > math.pi:
        x_rot = x_rot - 2*math.pi
    
    return '"%s" : { "x" : %f, "y" : %f, "z" : %f, "yaw" : %f }' % (c, x, y, z, x_rot)
    
    
def setup_gui():
    global CONTROL_WINDOW_NAME
    global CAMERA_SELECTOR_TRACKBAR_NAME
    global CANNY_MIN_TRACKBAR_NAME
    global CANNY_MAX_TRACKBAR_NAME

    cv2.namedWindow(CONTROL_WINDOW_NAME)
    cv2.createTrackbar(CAMERA_SELECTOR_TRACKBAR_NAME, CONTROL_WINDOW_NAME, DEFAULT_CAMERA, 3, camera_selector_callback)
    cv2.createTrackbar(CANNY_MIN_TRACKBAR_NAME, CONTROL_WINDOW_NAME, 120, 255, trackbar_callback)
    cv2.createTrackbar(CANNY_MAX_TRACKBAR_NAME, CONTROL_WINDOW_NAME, 180, 255, trackbar_callback)
    
    cv2.namedWindow(IMAGE_WINDOW_NAME)
    cv2.setMouseCallback(IMAGE_WINDOW_NAME, mouse_callback)


    camera_selector_callback(DEFAULT_CAMERA) # default to the first camera value
    time.sleep(2)

def close_gui():
    global g_camera
    
    g_camera.release()
    cv2.destroyAllWindows()
