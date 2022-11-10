# coding-challenge-cones

answer.png:
Uploaded as file to git

Methodology:
- read the image after downloading it into the project
- converting the image to HSV from BGR
- creating a mask, covering the orange color of the cones
      - binarized the iamge using the inrange function and the bitwise_and
- now that the image is black and white, erode and dilate image
- blur the image using bilateral filer and gaussian blur to ready the image
- apply canny after image has been optimized
- find the contours of the new canny image
- because there will be generally two lines of cones closing a car in...
      - created let and right list to append cones too
- sorted the contours from left to right and bottom to top
      - the two topmost cones are the end of the left list and start of right
      - sort the two topmost contours from left to right
- iterate through the contours
      - convert each contour to an approximate polygon, then convexHull
      - if the convexHull has above three and below eight points, it works
            - helps filter out unnecessary contours
      - add convexHull to left list, till you reach the top-right most cone
            - then you start adding to the right list

- now draw line between the endpoint cones of each the left and right lists
      - calculate slope of the line with rise over run
      - extend line segment by drawing it outside of image boundaries so it looks like a line
      - grab x and y coordinates to do this my using moments function of respective cones' contours
- write the image to a file and save it as answer.png

Previous Methods Used / What I Learned
- had to learn OpenCV for the first time
- tried applying filter methods on grayscale image instead of hsv
      - doesn't translate well for the rest of the process
- did not use color thresholding, which led to huge problems in disregarding the background contours
- tried segmenting the left and right lists by just halving the amount of contours
      - because my previous methods weren't perfect, there were still some cones which had multiple contours on them
      - this would throw off halving because it led to cones on the right side being added to the left list
- tried just drawing a line segment between the endpoint cones of the left and right
      - does not extend long enough to match what the answer should 

Libraries Used:
OpenCV
Numpy
