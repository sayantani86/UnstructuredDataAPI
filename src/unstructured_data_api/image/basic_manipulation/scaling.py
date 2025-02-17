import numpy as np
import cv2

def shrink_image(img):
    if not isinstance(img, np.ndarray):
        img = np.array(img)
        
    return cv2.resize(img, None, fx=2, fy=2, interpolation = cv2.INTER_AREA)

def resize(img):
    if not isinstance(img, np.ndarray):
        img = np.array(img)
        
    return cv2.resize(img, None, fx=2, fy=2, interpolation = cv2.INTER_CUBIC)

def zoom_image(img):
    if not isinstance(img, np.ndarray):
        img = np.array(img)
        
    height, width = img.shape[:2]
    return cv2.resize(img, (2*width, 2*height), interpolation = cv2.INTER_CUBIC)

