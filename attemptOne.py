import cv2 as cv
import numpy as np

# reading the image with cones
img = cv.imread('/Users/vithulravivarma/OpenCVPractice/red.png')
cv.imshow('Original', img)
height = img.shape[0]
width = img.shape[1]

# converting to HSV colors
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
cv.imshow('HSV', hsv)

# creating mask for binarization
lower = np.array([0, 170, 140])
upper = np.array([180, 240, 255])
mask = cv.inRange(hsv, lower, upper)
res = cv.bitwise_and(img, img, mask = mask)
cv.imshow('mask', mask)
cv.imshow('res', res)

# eroding and dilating
kernel = np.ones((1, 1), np.uint8)
erode = cv.erode(res, kernel)
dilate = cv.erode(erode, kernel)

# gaussian blur
bilateral = cv.bilateralFilter(res, 5, 225, 225)
cv.imshow('bilateral', bilateral)
gaussian = cv.GaussianBlur(bilateral, (7,7), cv.BORDER_DEFAULT)
cv.imshow('Gaussian', gaussian)

# canny edge detection
canny = cv.Canny(gaussian, 0, 255)
cv.imshow('Canny', canny)

# create contours
contours, hierarchies = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
print(f'{len(contours)} contour(s) found!')


blank = np.zeros(img.shape, dtype='uint8')

left = []
right = []
reverse = False
i = 0
length = 0

# cnts1 is contours sorted left to right
boundingBoxes1 = [cv.boundingRect(c) for c in contours]
(cnts1, boundingBoxes1) = zip(*sorted(zip(contours, boundingBoxes1),
	key=lambda b:b[1][i], reverse=reverse))


# cnts2 is contours sorted from bottom to top
reverse = True
i = 1
boundingBoxes2 = [cv.boundingRect(c) for c in contours]
(cnts2, boundingBoxes2) = zip(*sorted(zip(contours, boundingBoxes2),
	key=lambda b:b[1][i], reverse=reverse))

# the partition between the left and right lane is between the topmost cones
# need to sort the topmost cones left to right
top1 = cnts2[len(cnts2) - 1]
top2 = cnts2[len(cnts2) - 2]
topmost = [top1, top2]
reverse = False
i = 0
boundingBoxes3 = [cv.boundingRect(c) for c in topmost]
(cnts3, boundingBoxes3) = zip(*sorted(zip(topmost, boundingBoxes3),
	key=lambda b:b[1][i], reverse=reverse))
top1 = topmost[0]
top2 = topmost[1]
inLeft = True

# using convexHull and approxPoly to make it more defined
for k in cnts1:
    approx = cv.approxPolyDP(k, (0.04 * cv.arcLength(k, True)), True)
    convexHull = cv.convexHull(approx)
    if (len(convexHull) > 3 and len(convexHull) < 8):
        cv.drawContours(blank, [convexHull], -1, (0,255,0), 1)
        x,y,w,h = cv.boundingRect(convexHull)
        ret = cv.matchShapes(k, top2, 1, 0.0) 
        print(ret)
        if (cv.matchShapes(k, top2, 1, 0.0) == 0.0):
            inLeft = False
        if inLeft == True:
            # cv.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
            left.append(k)
        else:
            # cv.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
            right.append(k)
            
            
# calculating slope
def slope(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return((y2-y1)/(x2-x1))

# extending line segment to outside of the boundaries so it looks like a line
# utilizing slope function to do this extension
def drawLineWithPoints(image,p1,p2):
    x1, y1=p1
    x2, y2=p2
    m = slope(p1,p2)
    h, w = image.shape[:2]
    cx1 = 0
    cy1 = -(x1 - 0) * m +y1
    cx2 = w
    cy2 = -(x2 - w) * m +y2
    cv.line(image, (int(cx1), int(cy1)), (int(cx2), int(cy2)), (0, 0, 255), 2)
    
    
# grabbing the x and y of the endpoint cones to create the line
def drawLine(img, side):
    M = cv.moments(side[0])
    cx1 = int(M['m10']/M['m00'])
    cy1 = int(M['m01']/M['m00'])
    M = cv.moments(side[len(side) - 1])
    cx2 = int(M['m10']/M['m00'])
    cy2 = int(M['m01']/M['m00'])
    cv.line(img, (cx1, cy1), (cx2, cy2), (0, 0, 255), thickness = 1) 
    drawLineWithPoints(img, (cx1, cy1), (cx2, cy2))
    
# calling draw line on the left and right set of cones
drawLine(img, left)
drawLine(img, right)

cv.imshow('Contours Drawn', blank)
cv.imshow('Contours Boxed', img)

# saving the answer to another image
cv.imwrite('/Users/vithulravivarma/OpenCVPractice/answer.png', img)

cv.waitKey(0)