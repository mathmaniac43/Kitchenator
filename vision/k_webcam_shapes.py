import argparse
import cv2
import imutils
import json
import math
import time

from k_vision_helpers import *

# Constants
DISTANCE_UNITS = "cm"
BLACK_GREEN_DISTANCE = 8.8
DISTANCE_TO_M = 0.01

ORIGIN_OFFSET_R_DIST = -13
ORIGIN_OFFSET_D_DIST =  0

MAX_SQUARE_AGE = 5 # loop iterations

PAIR_TOL = 0.3
PAIR_ANGLE_TOL_DEG = 20

BLACK_GREEN_SPACING_RATIO = 1.2 # MAKE SURE IT IS A FLOATING POINT RATIO
BLACK_ORANGE_SPACING_RATIO = 1.2
BLACK_BLUE_SPACING_RATIO = 1.1
BLACK_PURPLE_SPACING_RATIO = 1.1

# Variables
origin_x = -1
origin_y = -1
origin_rot = 0

green_x = -1
green_y = -1
green_rot = 0

orange_x = -1
orange_y = -1
orange_rot = 0
orange_json = '"orange" : null'

blue_x = -1
blue_y = -1
blue_rot = 0
blue_json = '"blue" : null'

purple_x = -1
purple_y = -1
purple_rot = 0
purple_json = '"purple" : null'

pixels_per_unit_length = -1

squares = []

setup_gui()

while True:
    # Stop acquiring and processing when the 'Q' key is pressed.
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    
    # Skip to the next iteration if an image can't be acquired.
    (grabbed, image) = camera().read()
    if not grabbed:
        print 'no image acquired'
        continue
    
    # Get current values for canny adjustment parameters.
    canny_min = cv2.getTrackbarPos(CANNY_MIN_TRACKBAR_NAME, CONTROL_WINDOW_NAME)
    canny_max = cv2.getTrackbarPos(CANNY_MAX_TRACKBAR_NAME, CONTROL_WINDOW_NAME)
    
    # Adjust and clone the image to be processed.
    image = cv2.flip(image, FLIP_VALUE)
    image = imutils.resize(image, width=IMAGE_WIDTH)#, height=IMAGE_HEIGHT)
    edited_image = image.copy() # Keep the original image for reference.
    
    # Detect all contours in the image.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, canny_min, canny_max, 1)
    (contours, _) = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = False)
    
    # Loop over the contours and find the squares.
    for c in contours:
        M = cv2.moments(c)
        if M["m00"] == 0:
            continue
        
        x = int(math.floor((M["m10"] / M["m00"])))
        y = int(math.floor((M["m01"] / M["m00"])))
        if (x < 0 or x >= IMAGE_WIDTH or
            y < 0 or y >= IMAGE_HEIGHT):
            continue
        
        #https://docs.opencv.org/2.4/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html
        approx = cv2.approxPolyDP(c, 0.01 * IMAGE_WIDTH, True)
        rect = cv2.minAreaRect(approx)
        
        if (not is_square(approx, rect, 0.1)):
            continue
        
        # Surround detected squares in white.
        cv2.drawContours(edited_image, [approx], -1, (0, 0, 0), 2)
        
        w = rect[1][0]
        h = rect[1][1]
        rot = rect[2]
        
        # This ordering is bad and should feel bad.
        (b, g, r) = image[y][x]
    
        s = Square(x=x, y=y, w=w, h=h, rot=rot, col=classify_color((r, g, b)), age=0)
            
        squares.append(s)
    
    # Detect black and green pair.
    (black, green) = find_pair(squares, "black", "green", BLACK_GREEN_SPACING_RATIO, PAIR_TOL, PAIR_ANGLE_TOL_DEG)
    green_update = (green != None)
    if green_update:
        squares.remove(black)
        squares.remove(green)
        
        green_x = black.x
        green_y = black.y
        (bk_gr, green_rot) = get_rectangle_for_squares(black, green)
        
        # Surround squares together in green rectangle.
        cv2.drawContours(edited_image, [bk_gr], -1, (0, 255, 0), 2)
    
        d = math.sqrt((black.x - green.x) ** 2 + (black.y - green.y) ** 2)
        pixels_per_unit_length = d / BLACK_GREEN_DISTANCE
        
        origin_offset_r = ORIGIN_OFFSET_R_DIST * pixels_per_unit_length
        origin_offset_d = ORIGIN_OFFSET_D_DIST * pixels_per_unit_length
        
        origin_rot = green_rot
        (origin_x, origin_y) = apply_transform((green_x, green_y), origin_rot, (origin_offset_r, origin_offset_d), True)
        
        # Yellow circle about the origin, signifying a live update.
        cv2.circle(edited_image, (origin_x, origin_y), 5, (0, 255, 255))
    
    # Gotta find the reference point first, or else the math breaks
    if pixels_per_unit_length < 0:
        print 'searching for reference'
        continue
    
    # Detect black and blue pair.
    (black, blue) = find_pair(squares, "black", "blue", BLACK_BLUE_SPACING_RATIO, PAIR_TOL, PAIR_ANGLE_TOL_DEG)
    blue_update = (blue != None)
    if blue_update:
        squares.remove(black)
        squares.remove(blue)
        
        blue_x = black.x
        blue_y = black.y
        (bk_br, blue_rot) = get_rectangle_for_squares(black, blue)
        
        # Surround squares together in blue rectangle.
        cv2.drawContours(edited_image, [bk_br], -1, (255, 0, 0), 2)
    
    # Detect black and orange pair.
    (black, orange) = find_pair(squares, "black", "orange", BLACK_ORANGE_SPACING_RATIO, PAIR_TOL, PAIR_ANGLE_TOL_DEG)
    orange_update = (orange != None)
    if orange_update:
        squares.remove(black)
        squares.remove(orange)
        
        orange_x = black.x
        orange_y = black.y
        (bk_rd, orange_rot) = get_rectangle_for_squares(black, orange)
        
        # Surround squares together in orange rectangle.
        cv2.drawContours(edited_image, [bk_rd], -1, (0, 0, 255), 2)
    
    # Detect black and purple pair.
    (black, purple) = find_pair(squares, "black", "purple", BLACK_PURPLE_SPACING_RATIO, PAIR_TOL, PAIR_ANGLE_TOL_DEG)
    purple_update = (purple != None)
    if purple_update:
        squares.remove(black)
        squares.remove(purple)
        
        purple_x = black.x
        purple_y = black.y
        (bk_rd, purple_rot) = get_rectangle_for_squares(black, purple)
        
        # Surround squares together in purple rectangle.
        cv2.drawContours(edited_image, [bk_rd], -1, (150, 0, 150), 2)
    
    # Update lifetime status of current squares.
    for i in range(len(squares)-1, -1, -1):
        square = squares.pop(i)
        
        if square.age >= MAX_SQUARE_AGE:
            continue
        else:
            square = square._replace(age=square.age+1)
            squares.append(square)
    
    # Label last known position of green.
    if green_x >= 0 and green_y >= 0:
        cv2.circle(edited_image, (green_x, green_y), 3, (0, 255, 0))
        
        (right, down) = inverse_transform((origin_x, origin_y), origin_rot, (green_x, green_y))
        right = right / pixels_per_unit_length
        down = down / pixels_per_unit_length
        
        green_json = to_position_json(
            "green",
            right * DISTANCE_TO_M,
            down * DISTANCE_TO_M,
            green_rot,
            origin_rot
        )
        
        cv2.putText(edited_image, green_json, (green_x + 5, green_y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)
    
    # Label last known position of orange.
    if orange_x >= 0 and orange_y >= 0:
        cv2.circle(edited_image, (orange_x, orange_y), 3, (0, 0, 255))
        
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
        cv2.putText(edited_image, orange_json, (orange_x + 5, orange_y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)
    
    # Label last known position of blue.
    if blue_x >= 0 and blue_y >= 0:
        cv2.circle(edited_image, (blue_x, blue_y), 3, (255, 80, 80))
        
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
        cv2.putText(edited_image, blue_json, (blue_x + 5, blue_y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 2)
    
    # Label last known position of purple.
    if purple_x >= 0 and purple_y >= 0:
        cv2.circle(edited_image, (purple_x, purple_y), 3, (150, 0, 150))
        
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
        cv2.putText(edited_image, purple_json, (purple_x + 5, purple_y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150, 0, 150), 2)
    
    # Handle json
    full_json = '{%s, %s, %s}' % (orange_json, blue_json, purple_json)
    print(full_json)
    
    # Label last known position of origin.
    if origin_x >= 0 and origin_y >= 0:
        cv2.circle(edited_image, (origin_x, origin_y), 3, (0, 255, 255))
        
        axis_distance = 5 * pixels_per_unit_length
        
        (right_x, right_y) = apply_transform(
            (origin_x, origin_y), origin_rot, (axis_distance, 0), True)
        cv2.circle(edited_image, (right_x, right_y), 3, (0, 255, 255))
        
        (down_x, down_y) = apply_transform(
            (origin_x, origin_y), origin_rot, (0, axis_distance), True)
        cv2.circle(edited_image, (down_x, down_y), 3, (0, 255, 255))
    
    # Print mouse hover information.
    if (mouse_x() >= 0 and mouse_x() < IMAGE_WIDTH and
        mouse_y() >= 0 and mouse_y() < IMAGE_HEIGHT):
        (mouse_b, mouse_g, mouse_r) = image[mouse_y()][mouse_x()]
        
        (right, down) = inverse_transform((origin_x, origin_y), origin_rot, (mouse_x(), mouse_y()))
        right = right / pixels_per_unit_length
        down = down / pixels_per_unit_length
        
        pos_str = 'r=%02.1f,d=%02.1f(%s)' % (
            right,
            down,
            DISTANCE_UNITS
        )
        
        s = ("x=" + str(mouse_x()) + " " +
             "y=" + str(mouse_y()) + " " +
             "c=" + classify_color((mouse_r, mouse_g, mouse_b)) + "? " +
             "r=" + str(mouse_r) + " " + 
             "g=" + str(mouse_g) + " " + 
             "b=" + str(mouse_b) + " " +
             pos_str)
        
        # Print latest mouse position information at the bottom of the screen.
        cv2.rectangle(edited_image, (0, IMAGE_HEIGHT - 20), (IMAGE_WIDTH, IMAGE_HEIGHT), (0, 0, 0), -1)
        cv2.putText(edited_image, s, (5, IMAGE_HEIGHT - 5), cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (255, 255, 255), 2)
    
    cv2.imshow(IMAGE_WINDOW_NAME, edited_image)
    cv2.namedWindow(CONTROL_WINDOW_NAME)

close_gui()