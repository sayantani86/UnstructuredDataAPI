import numpy as np
import cv2

def erode(img):
    """It erodes away the boundaries of foreground object"""
    
    if not isinstance(img, np.ndarray):
        img = np.array(img)
    
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(img,kernel,iterations = 1)


def dilate(img):
    """It erodes away the boundaries of foreground object"""
    
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(img,kernel,iterations = 1)