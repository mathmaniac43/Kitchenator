import argparse
import cv2
import imutils
import math
import time

from pyimagesearch.shapedetector import ShapeDetector

mouse_x, mouse_y = -1, -1
def mouse_callback(event, x, y, flags, param):
    global mouse_x, mouse_y
    
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_x = x
        mouse_y = y
        
def trackbar_callback(val):
    pass
        
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480
WINDOW_NAME = "Image"
CANNY_MIN_TRACKBAR_NAME = "Canny Min"
CANNY_MAX_TRACKBAR_NAME = "Canny Max"
AREA_MIN_TRACKBAR_NAME = "Area Min"
AREA_MAX_TRACKBAR_NAME = "Area Max"

cv2.namedWindow(WINDOW_NAME)
cv2.setMouseCallback(WINDOW_NAME, mouse_callback)
cv2.createTrackbar(CANNY_MIN_TRACKBAR_NAME, WINDOW_NAME, 120, 255, trackbar_callback)
cv2.createTrackbar(CANNY_MAX_TRACKBAR_NAME, WINDOW_NAME, 180, 255, trackbar_callback)
cv2.createTrackbar(AREA_MIN_TRACKBAR_NAME,  WINDOW_NAME, 70,  200, trackbar_callback)
cv2.createTrackbar(AREA_MAX_TRACKBAR_NAME,  WINDOW_NAME, 90,  200, trackbar_callback)

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
    
    edged = cv2.Canny(blurred, canny_min, canny_max)
    (contours, _) = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = False)
    
    if (mouse_x >= 0 and mouse_x < IMAGE_WIDTH and
        mouse_y >= 0 and mouse_y < IMAGE_HEIGHT):
        
        (mouse_r, mouse_g, mouse_b) = image[mouse_y][mouse_x]
        
        s = ("x=" + str(mouse_x) + " " +
             "y=" + str(mouse_y) + " " +
             "r=" + str(mouse_r) + " " +
             "g=" + str(mouse_g) + " " +
             "b=" + str(mouse_b))
        
        # Print color information where mouse is
        cv2.putText(image, s, (5, IMAGE_HEIGHT - 5), cv2.FONT_HERSHEY_SIMPLEX,
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
        
        area = cv2.contourArea(c)
        if (area < area_min or area > area_max):
            continue
        
        shape = sd.detect(c)
        if not shape == 'square':
            continue
            
        (r, g, b) = image[y][x]
        
        s = ("x=" + str(x) + " " +
             "y=" + str(y) + " " +
             "r=" + str(r) + " " +
             "g=" + str(g) + " " +
             "b=" + str(b) + " " +
             "A=" + str(area))
        
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        cv2.putText(image, s, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (255, 255, 255), 2)
    
    cv2.imshow(WINDOW_NAME, image)

camera.release()
cv2.destroyAllWindows()
