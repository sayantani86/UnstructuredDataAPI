import numpy as np
import cv2

def erode(img):
    """It erodes away the boundaries of foreground object"""
    
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(img,kernel,iterations = 1)

def dilate(img):
    """a pixel element is ‘1’ if atleast one pixel under the kernel is ‘1’. So it increases the white region in the image or size of foreground object increases. Normally, in cases like noise removal, erosion is followed by dilation"""
    
    return cv2.dilate(img,kernel,iterations = 1)