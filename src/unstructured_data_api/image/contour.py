import numpy as np
import cv2

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
    
    cv2.drawContours(img, contours, contour_num, (0,255,0), 3)
    
    return img

