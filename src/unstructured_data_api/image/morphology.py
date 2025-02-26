import numpy as np
import cv2

def erode(img, kernel=np.ones((5,5),np.uint8)):
    """It erodes away the boundaries of foreground object"""
    
    return cv2.erode(img,kernel,iterations = 1)


def dilate(img, kernel=np.ones((5,5),np.uint8)):
    """It erodes away the boundaries of foreground object"""
    
    return cv2.dilate(img,kernel,iterations = 1)

def opening(img, kernel=np.ones((5,5),np.uint8)):
    """Another term for erosion followed by dilation"""
    
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

def closing(img, kernel = np.ones((5,5),np.uint8)):
    """Another term for erosion followed by dilation"""
    
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)