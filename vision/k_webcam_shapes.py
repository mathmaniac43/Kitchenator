import argparse
import cv2
import imutils
import math

from pyimagesearch.shapedetector import ShapeDetector

camera = cv2.VideoCapture(0)
camera.set(cv2.cv.CV_CAP_PROP_FPS, 2)
camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,  640)
camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)

sd = ShapeDetector()
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    
    (grabbed, image) = camera.read()
    if not grabbed:
        break
        
    image = cv2.flip(image, 1)
    
    resized = image
    ratio = 1
    #resized = imutils.resize(image, width=500)
    #ratio = image.shape[0] / float(resized.shape[0])
    
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("gray", gray)
    
    blurred = cv2.bilateralFilter(gray, 11, 17, 17)
    #cv2.imshow("blurred", blurred)
    
    edged = cv2.Canny(blurred, 30, 200)
    #(contours, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    (contours, _) = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = False)
    
    #shapes = {'circle':[], 'triangle':[], 'square':[], 'rectangle':[], 'pentagon':[]}
    # loop over the contours
    for c in contours:
	    M = cv2.moments(c)
	    if M["m00"] == 0:
	        continue
	    
	    cX = int(math.floor((M["m10"] / M["m00"]) * ratio))
	    cY = int(math.floor((M["m01"] / M["m00"]) * ratio))
	    
	    if cX < 0 or cX >= len(resized) or cY < 0 or cY >= len(resized[0]):
	        continue
		    
	    (r, g, b) = image[cX][cY]
	    
	    # only continue if reddish
	    if not (r > 100 and (r > g or r > b)):
	        continue
	    
	    shape = sd.detect(c)
	    
	    # only continue if squareish
	    #if not shape == 'square':
	    #    continue
	    
	    # only continue if rectangularish
	    if not shape == 'rectangle':
	        continue
	    
	    print((r, g, b))
	    
	    #shapes[shape].append((cX, cY))
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
