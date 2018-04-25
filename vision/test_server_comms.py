import argparse
import cv2
import imutils
import json
import math
import time

from k_vision_helpers import *

# Constants
DISTANCE_UNITS = "cm"
BLACK_GREEN_DISTANCE = 7 * 2.54
DISTANCE_TO_M = 0.01

# Variables
origin_x = 200
origin_y = 300
origin_rot = math.pi/2

#green_x = 300
#green_y = 300
#green_rot = 0

orange_x = 10
orange_y = 47
orange_rot = -math.pi/7

blue_x = 100
blue_y = 100
blue_rot = -12 * math.pi / 180

purple_x = 300
purple_y = 300
purple_rot = math.pi

pixels_per_unit_length = 35

# todo: properly test some cardinal directions and ensure that the transform works properly


# Green doesn't matter since it determines the origin

#(right, down) = inverse_transform((origin_x, origin_y), origin_rot, (green_x, green_y))
#right = right / pixels_per_unit_length
#down = down / pixels_per_unit_length
#
#green_json = to_position_json(
#    "green",
#    right * DISTANCE_TO_M,
#    down * DISTANCE_TO_M,
#    numpy.rad2deg(green_rot)
#)
#print(green_json)



(right, down) = inverse_transform((origin_x, origin_y), origin_rot, (orange_x, orange_y))
right = right / pixels_per_unit_length
down = down / pixels_per_unit_length

orange_json = to_position_json(
    "orange",
    right * DISTANCE_TO_M,
    down * DISTANCE_TO_M,
    orange_rot,
    origin_rot
)
print(orange_json)



(right, down) = inverse_transform((origin_x, origin_y), origin_rot, (blue_x, blue_y))
right = right / pixels_per_unit_length
down = down / pixels_per_unit_length

blue_json = to_position_json(
    "blue",
    right * DISTANCE_TO_M,
    down * DISTANCE_TO_M,
    blue_rot,
    origin_rot
)
print(blue_json)



(right, down) = inverse_transform((origin_x, origin_y), origin_rot, (purple_x, purple_y))
right = right / pixels_per_unit_length
down = down / pixels_per_unit_length

purple_json = to_position_json(
    "purple",
    right * DISTANCE_TO_M,
    down * DISTANCE_TO_M,
    purple_rot,
    origin_rot
)
print(purple_json)

full_json = '{%s, %s, %s}' % (orange_json, blue_json, purple_json)