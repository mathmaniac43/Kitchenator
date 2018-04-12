import argparse
import cv2
import imutils
import math
import time

g_mouse_x, g_mouse_y = -1, -1
def mouse_callback(event, x, y, flags, param):
    global g_mouse_x, g_mouse_y
    
    if event == cv2.EVENT_MOUSEMOVE:
        g_mouse_x = x
        g_mouse_y = y
        
def trackbar_callback(val):
    pass

g_camera = None
def camera_selector_callback(val):
    global g_camera
    
    if g_camera != None:
        g_camera.release()
    
    g_camera = cv2.VideoCapture(val)
    g_camera.set(cv2.cv.CV_CAP_PROP_FPS, 2)
    g_camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,  IMAGE_WIDTH)
    g_camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, IMAGE_HEIGHT)

def is_square(points, tol):
    if len(points) == 4:
        rect = cv2.minAreaRect(points) # ((x,y), (w,h), rot)
        w = rect[1][0]
        h = rect[1][1]
        m = min((w, h))
        return (m * tol > abs(w - h))
    
    return False

def get_RGB_string(requested_color):
    return 'R%03d G%03d B%03d' % requested_color
        
IMAGE_WIDTH = 1920/2#640
IMAGE_HEIGHT = 1080/2#480
WINDOW_NAME = "Image"
CONTROL_WINDOW_NAME = "Controls"
CAMERA_SELECTOR_TRACKBAR_NAME = "Choose Camera Index"
CANNY_MIN_TRACKBAR_NAME = "Canny Min"
CANNY_MAX_TRACKBAR_NAME = "Canny Max"
AREA_MIN_TRACKBAR_NAME = "Area Min"
AREA_MAX_TRACKBAR_NAME = "Area Max"

RED_BLACK_dANCE_M = 0.033

PIXELS_PER_M = None
RED_X_M = None
RED_Y_M = None

COLOR_THRESHOLD = 60
BLUE_THRESHOLD = COLOR_THRESHOLD + 15

cv2.namedWindow(WINDOW_NAME)
cv2.setMouseCallback(WINDOW_NAME, mouse_callback)

cv2.namedWindow(CONTROL_WINDOW_NAME)
cv2.createTrackbar(CAMERA_SELECTOR_TRACKBAR_NAME, CONTROL_WINDOW_NAME, 1, 3, camera_selector_callback)
cv2.createTrackbar(CANNY_MIN_TRACKBAR_NAME, CONTROL_WINDOW_NAME, 120, 255, trackbar_callback)
cv2.createTrackbar(CANNY_MAX_TRACKBAR_NAME, CONTROL_WINDOW_NAME, 180, 255, trackbar_callback)
cv2.createTrackbar(AREA_MIN_TRACKBAR_NAME,  CONTROL_WINDOW_NAME, 120, 600, trackbar_callback)
cv2.createTrackbar(AREA_MAX_TRACKBAR_NAME,  CONTROL_WINDOW_NAME, 180, 600, trackbar_callback)

camera_selector_callback(cv2.getTrackbarPos(CAMERA_SELECTOR_TRACKBAR_NAME, CONTROL_WINDOW_NAME)) # default to the first camera value
time.sleep(2)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    
    (grabbed, image) = g_camera.read()
    if not grabbed:
        continue
        
    canny_min = cv2.getTrackbarPos(CANNY_MIN_TRACKBAR_NAME, CONTROL_WINDOW_NAME)
    canny_max = cv2.getTrackbarPos(CANNY_MAX_TRACKBAR_NAME, CONTROL_WINDOW_NAME)  
    area_min = cv2.getTrackbarPos(AREA_MIN_TRACKBAR_NAME,   CONTROL_WINDOW_NAME)  
    area_max = cv2.getTrackbarPos(AREA_MAX_TRACKBAR_NAME,   CONTROL_WINDOW_NAME)
    
    image = cv2.flip(image, 1)
    
    image = imutils.resize(image, width=IMAGE_WIDTH, height=IMAGE_HEIGHT)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.bilateralFilter(gray, 11, 17, 17)
    
    edged = cv2.Canny(blurred, canny_min, canny_max, 1)
    (contours, _) = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = False)
    
    edited_image = image.copy()
    
    if (g_mouse_x >= 0 and g_mouse_x < IMAGE_WIDTH and
        g_mouse_y >= 0 and g_mouse_y < IMAGE_HEIGHT):
        
        (mouse_b, mouse_g, mouse_r) = image[g_mouse_y][g_mouse_x]
        
        s = ("x=" + str(g_mouse_x) + " " +
             "y=" + str(g_mouse_y) + " " +
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
            
        rect = cv2.minAreaRect(approx)
        
        w = rect[1][0]
        h = rect[1][1]
        
        # This ordering is bad and should feel bad.
        (b, g, r) = image[y][x]
            
        tuple = (x, y, w, h, area, (r, g, b))
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
        
        cv2.drawContours(edited_image, [approx], -1, (0, 0, 255), 2)
    
    done = False
    for (rx, ry, rw, rh, _, _) in red_squares:
        for (bx, by, _, _, _, _) in black_squares:
            d = math.sqrt((bx - rx) ** 2 + (by - ry) ** 2)
            m = min((rw, rh))
            if d < m * 1.5:
                PIXELS_PER_M = d / RED_BLACK_dANCE_M
                done = True
                break
            
        if done:
            break
            
    cv2.putText(edited_image, str(PIXELS_PER_M), (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    for (x, y, w, h, A, col) in (black_squares + red_squares + green_squares + blue_squares):
        s = ("x=" + str(x) + " " +
             "y=" + str(y) + " " +
             "A=" + str(area) + " " +
             "c=" + get_RGB_string(col))
             
        print s
        
        cv2.putText(edited_image, s, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (255, 255, 255), 2)
    
    cv2.imshow(WINDOW_NAME, edited_image)
    cv2.namedWindow(CONTROL_WINDOW_NAME)
