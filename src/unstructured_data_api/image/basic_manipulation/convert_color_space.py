import numpy as np

"""This module converts teh color space of an image whoch is helpful for tasks like thresholding, edge detection, and object tracking"""

def convert_BGR_to_GRAY(image):
    """Image load by opencv.It converts BGR to Grayscale."""

    if not isinstance(image, np.ndarray):
        image = np.array(image)
        
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def convert_RGB_to_GRAY(image):
    """Image load by opencv.It converts RGB to Grayscale"""

    if not isinstance(image, np.ndarray):
        image = np.array(image)
        
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

def convert_RGB_to_HSV(im):
    """Image load by opencv.It converts RGB to HSV"""
    
    if not isinstance(image, np.ndarray):
        image = np.array(image)
        
    return cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

def convert_RGB_to_LAB(im):
    """Image load by opencv.It converts RGB to LAB"""
    
    if not isinstance(image, np.ndarray):
        image = np.array(image)
        
    return cv2.cvtColor(image, cv2.COLOR_RGB2LAB)

def convert_RGB_to_HSV_with_PIL(im):
    """Image load by PIL"""
    
    return im.convert('HSV')