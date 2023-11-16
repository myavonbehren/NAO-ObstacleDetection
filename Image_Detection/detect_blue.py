import cv2 as cv
import numpy as np

def detect(filename):
    '''
    Load an image using OpenCV and detect the presence of the color blue.

    Args:
        filename (str): The path to the image file.

    Returns:
        bool: True if blue color is detected, False otherwise.
    '''
    image = cv.imread(filename)

    if image is None:
        print("Image not found or could not be loaded.")
    else:
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

        lower_blue = np.array([110, 50, 50])
        upper_blue = np.array([130, 255, 255])

        mask = cv.inRange(hsv, lower_blue, upper_blue)
        res = cv.bitwise_and(image, image, mask=mask)

        pixels = cv.countNonZero(mask)
        
##        Uncomment the following lines to display the images
        
##        cv.imshow('frame', image)
##        cv.imshow('mask', mask)
##        cv.imshow('res', res)
##        k = cv.waitKey(0) & 0xFF
##        cv.destroyAllWindows()

        return pixels > 1000:
            
