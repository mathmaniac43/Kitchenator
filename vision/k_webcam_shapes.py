import argparse
import cv2
import imutils
import math
import time
import webcolors

from pyimagesearch.shapedetector import ShapeDetector

mouse_x, mouse_y = -1, -1
def mouse_callback(event, x, y, flags, param):
    global mouse_x, mouse_y
    
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_x = x
        mouse_y = y
        
def trackbar_callback(val):
    pass

def is_square(points, tol):
    if len(points) == 4:
        rect = cv2.minAreaRect(points) # ((x,y), (w,h), rot)
        m = min(rect[1])
        return (m * tol > abs(rect[1][0] - rect[1][1]))
    
    return False

def get_RGB_string(requested_color):
    return 'R%03d G%03d B%03d' % requested_color
        
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480
WINDOW_NAME = "Image"
CANNY_MIN_TRACKBAR_NAME = "Canny Min"
CANNY_MAX_TRACKBAR_NAME = "Canny Max"
AREA_MIN_TRACKBAR_NAME = "Area Min"
AREA_MAX_TRACKBAR_NAME = "Area Max"

COLOR_THRESHOLD = 50
BLUE_THRESHOLD = COLOR_THRESHOLD + 15

cv2.namedWindow(WINDOW_NAME)
cv2.setMouseCallback(WINDOW_NAME, mouse_callback)
cv2.createTrackbar(CANNY_MIN_TRACKBAR_NAME, WINDOW_NAME, 120, 255, trackbar_callback)
cv2.createTrackbar(CANNY_MAX_TRACKBAR_NAME, WINDOW_NAME, 180, 255, trackbar_callback)
cv2.createTrackbar(AREA_MIN_TRACKBAR_NAME,  WINDOW_NAME, 120, 300, trackbar_callback)
cv2.createTrackbar(AREA_MAX_TRACKBAR_NAME,  WINDOW_NAME, 180, 300, trackbar_callback)

camera = cv2.VideoCapture(1)
camera.set(cv2.cv.CV_CAP_PROP_FPS, 2)
camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,  IMAGE_WIDTH)
camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, IMAGE_HEIGHT)

time.sleep(2)

sd = ShapeDetector()
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    
    (grabbed, image) = camera.read()
    if not grabbed:
        continue
        
    canny_min = cv2.getTrackbarPos(CANNY_MIN_TRACKBAR_NAME, WINDOW_NAME)
    canny_max = cv2.getTrackbarPos(CANNY_MAX_TRACKBAR_NAME, WINDOW_NAME)  
    area_min = cv2.getTrackbarPos(AREA_MIN_TRACKBAR_NAME, WINDOW_NAME)  
    area_max = cv2.getTrackbarPos(AREA_MAX_TRACKBAR_NAME, WINDOW_NAME)
    
    image = cv2.flip(image, -1)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.bilateralFilter(gray, 11, 17, 17)
    
    edged = cv2.Canny(blurred, canny_min, canny_max, 1)
    (contours, _) = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = False)
    
    edited_image = image.copy()
    
    if (mouse_x >= 0 and mouse_x < IMAGE_WIDTH and
        mouse_y >= 0 and mouse_y < IMAGE_HEIGHT):
        
        (mouse_b, mouse_g, mouse_r) = image[mouse_y][mouse_x]
        
        s = ("x=" + str(mouse_x) + " " +
             "y=" + str(mouse_y) + " " +
             "c=" + get_RGB_string((mouse_r, mouse_g, mouse_b)))
        
        # Print color information where mouse is
        cv2.putText(edited_image, s, (5, IMAGE_HEIGHT - 5), cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (255, 255, 255), 2)
    
    black_squares = []
    green_squares = []
    blue_squares = []
    red_squares = []
    
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
        
        area = cv2.contourArea(c)
        if (area < area_min or area > area_max):
            continue
        
        #https://docs.opencv.org/2.4/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html
        approx = cv2.approxPolyDP(c, 0.01 * IMAGE_WIDTH, True)
        
        if (not is_square(approx, 0.2)):
            continue
        
        # This ordering is bad and should feel bad.
        (b, g, r) = image[y][x]
            
        tuple = (x, y, area)
        if (r < COLOR_THRESHOLD and
            g < COLOR_THRESHOLD and
            b < COLOR_THRESHOLD):
            black_squares.append(tuple)
            color_name = "black"
        elif (r > COLOR_THRESHOLD and
              g < COLOR_THRESHOLD and
              b < COLOR_THRESHOLD):
            red_squares.append(tuple)
            color_name = "red"
        elif (r < COLOR_THRESHOLD and
              g > COLOR_THRESHOLD and
              b < COLOR_THRESHOLD):
            green_squares.append(tuple)
            color_name = "green"
        elif (r < BLUE_THRESHOLD and
              g < BLUE_THRESHOLD and
              b > BLUE_THRESHOLD):
            blue_squares.append(tuple)
            color_name = "blue"
        else:
            color_name = get_RGB_string((r, g, b))
        
        s = ("x=" + str(x) + " " +
             "y=" + str(y) + " " +
             "A=" + str(area) + " " +
             "c=" + color_name)
        
        cv2.drawContours(edited_image, [approx], -1, (0, 0, 255), 2)

        cv2.putText(edited_image, s, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (255, 255, 255), 2)
    
    cv2.imshow(WINDOW_NAME, edited_image)

camera.release()
cv2.destroyAllWindows()
