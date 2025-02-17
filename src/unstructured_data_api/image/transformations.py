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

def getRectKernel():
    return cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))

def getEllipticalKernel():
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))

def getCrossShapedKernel():
    return cv2.getStructuringElement(cv2.MORPH_CROSS,(5,5))

def findContours(thresh):
    """
    im2: A modified image
    contours: Python list of all the contours in the image
    hierarchy: 
    """
    
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    return contours, hierarchy

def drawContours(img, contours, contour_num=-1):
    """
    img: Original image
    """
    
    if contour_num != -1:
        return cv2.drawContours(img, contours[contour_num], contour_num, (0,255,0), 3)
    
    return cv2.drawContours(img, contours, contour_num, (0,255,0), 3)

