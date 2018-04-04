# USAGE
# python detect_shapes.py --image shapes_and_colors.png

# import the necessary packages
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import cv2

import time

# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,
#	help="path to the input image")
#args = vars(ap.parse_args())

camera = cv2.VideoCapture(0)
camera.set(cv2.cv.CV_CAP_PROP_FPS, 2)
camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,  640)
camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
#time.sleep(2.5)

sd = ShapeDetector()
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    
    (grabbed, image) = camera.read()
    if not grabbed:
        break
    
    resized = imutils.resize(image, width=500)
    #cv2.imshow("testing", resized)
    
    ratio = image.shape[0] / float(resized.shape[0])
    
    # convert the resized image to grayscale, blur it slightly,
    # and threshold it
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray", gray)
    
    blurred = cv2.bilateralFilter(gray, 11, 17, 17)
    cv2.imshow("blurred", blurred)
    
    edged = cv2.Canny(blurred, 30, 200)
    
    #thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    #cv2.imshow("thresh", thresh)

    # find contours in the thresholded image and initialize the
    # shape detector
    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = False)
    
    shapes = {'circle':[], 'triangle':[], 'square':[], 'rectangle':[], 'pentagon':[]}
    # loop over the contours
    for c in cnts:
	    # compute the center of the contour, then detect the name of the
	    # shape using only the contour
	    M = cv2.moments(c)
	    if M["m00"] == 0:
	        continue
	    #print M
	    
	    cX = int((M["m10"] / M["m00"]) * ratio)
	    cY = int((M["m01"] / M["m00"]) * ratio)
	    shape = sd.detect(c)
	    
	    shapes[shape].append((cX, cY))
	    
	    #if shape == 'circle' and 
	    #print shapes

	    # multiply the contour (x, y)-coordinates by the resize ratio,
	    # then draw the contours and the name of the shape on the image
	    c = c.astype("float")
	    c *= ratio
	    c = c.astype("int")
	    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	    cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
		    0.5, (255, 255, 255), 2)

    # show the output image
    cv2.imshow("Image", image)

camera.release()
cv2.destroyAllWindows()
