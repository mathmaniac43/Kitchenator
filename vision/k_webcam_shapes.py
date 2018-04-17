import argparse
import cv2
import imutils
import math
import time

from k_vision_helpers import *

DISTANCE_UNITS = "cm"
BLACK_GREEN_DISTANCE = 7 * 2.54

ORIGIN_OFFSET_R_DIST = -13.5
ORIGIN_OFFSET_D_DIST =  0

setup_gui()

squares = []

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    
    (grabbed, image) = camera().read()
    if not grabbed:
        continue
        
    canny_min = cv2.getTrackbarPos(CANNY_MIN_TRACKBAR_NAME, CONTROL_WINDOW_NAME)
    canny_max = cv2.getTrackbarPos(CANNY_MAX_TRACKBAR_NAME, CONTROL_WINDOW_NAME)
    
    image = cv2.flip(image, 1)
    
    image = imutils.resize(image, width=IMAGE_WIDTH)#, height=IMAGE_HEIGHT)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #blurred = cv2.bilateralFilter(gray, 11, 17, 17)
    blurred = gray
    
    edged = cv2.Canny(blurred, canny_min, canny_max, 1)
    (contours, _) = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = False)
    
    edited_image = image.copy()
    
    if (mouse_x() >= 0 and mouse_x() < IMAGE_WIDTH and
        mouse_y() >= 0 and mouse_y() < IMAGE_HEIGHT):
        (mouse_b, mouse_g, mouse_r) = image[mouse_y()][mouse_x()]
        
        s = ("x=" + str(mouse_x()) + " " +
             "y=" + str(mouse_y()) + " " +
             "c=" + classify_color((mouse_r, mouse_g, mouse_b)) + "? " +
             "r=" + str(mouse_r) + " " + 
             "g=" + str(mouse_g) + " " + 
             "b=" + str(mouse_b))
        
        # Print color information where mouse is
        cv2.rectangle(edited_image, (0, IMAGE_HEIGHT - 20), (IMAGE_WIDTH, IMAGE_HEIGHT), (0, 0, 0), -1)
        cv2.putText(edited_image, s, (5, IMAGE_HEIGHT - 5), cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (255, 255, 255), 2)
    
    # Loop over the contours
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
            
        cv2.drawContours(edited_image, [approx], -1, (0, 0, 255), 2)
        
        w = rect[1][0]
        h = rect[1][1]
        rot = rect[2]
        
        # This ordering is bad and should feel bad.
        (b, g, r) = image[y][x]
    
        s = Square(x=x, y=y, w=w, h=h, rot=rot, col=classify_color((r, g, b)), age=0)
            
        squares.append(s)
    
    PAIR_TOL = 0.2
    
    (black, green) = find_pair(squares, "black", "green", 7.0/3, PAIR_TOL)
    if black != None:
        squares.remove(black)
        squares.remove(green)
        
        (bk_gr, rot) = get_rectangle_for_squares(black, green)
        cv2.drawContours(edited_image, [bk_gr], -1, (0, 255, 0), 2)
    
        d = math.sqrt((black.x - green.x) ** 2 + (black.y - green.y) ** 2)
        PIXEL_DENSITY = d / BLACK_GREEN_DISTANCE
        #print("%f pixels per %s" % (PIXEL_DENSITY, DISTANCE_UNITS))
        
        origin_offset_r = ORIGIN_OFFSET_R_DIST * PIXEL_DENSITY
        origin_offset_d = ORIGIN_OFFSET_D_DIST * PIXEL_DENSITY
        
        origin_x = black.x + int(round(math.cos(rot) * origin_offset_r - math.sin(rot) * origin_offset_d))
        origin_y = black.y + int(round(math.cos(rot) * origin_offset_d + math.sin(rot) * origin_offset_r))
        
        cv2.circle(edited_image, (origin_x, origin_y), 5, (0, 0, 0))
        
    (black, blue) = find_pair(squares, "black", "blue", 1.1, PAIR_TOL)
    if black != None:
        squares.remove(black)
        squares.remove(blue)
        
        (bk_br, rot) = get_rectangle_for_squares(black, blue)
        cv2.drawContours(edited_image, [bk_br], -1, (255, 0, 0), 2)
    
    (black, red) = find_pair(squares, "black", "red", 9, PAIR_TOL)
    if black != None:
        squares.remove(black)
        squares.remove(red)
        
        (bk_rd, rot) = get_rectangle_for_squares(black, red)
        cv2.drawContours(edited_image, [bk_rd], -1, (0, 0, 255), 2)
    
    for i in range(len(squares)-1, -1, -1):
        square = squares.pop(i)
        
        if square.age >= 3:
            continue
        else:
            square = square._replace(age=square.age+1)
            squares.append(square)
    
    cv2.imshow(IMAGE_WINDOW_NAME, edited_image)
    cv2.namedWindow(CONTROL_WINDOW_NAME)
