import numpy as np
import cv2

def thresh_binary(im):
    if not isinstance(im, np.ndarray):
        im = np.array(im)
        
    return cv2.threshold(im, 127, 255, cv2.THRESH_BINARY)

def thresh_binaryInv(im):
    if not isinstance(im, np.ndarray):
        im = np.array(im)
        
    return cv2.threshold(im, 127, 255, cv2.THRESH_BINARY_INV)

def thresh_trunc(im):
    if not isinstance(im, np.ndarray):
        im = np.array(im)
    return cv2.threshold(im, 127, 255, cv2.THRESH_TRUNC)

def thresh_to_zero(im):
    if not isinstance(im, np.ndarray):
        im = np.array(im)
        
    return cv2.threshold(im, 127, 255, cv2.THRESH_TOZERO)

def thresh_to_zero_inv(im):
    if not isinstance(im, np.ndarray):
        im = np.array(im)
        
    return cv2.threshold(im, 127, 255, cv2.THRESH_TOZERO_INV)

def thresh_adaptive_mean(im):
    if not isinstance(im, np.ndarray):
        im = np.array(im)
        
    return cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)

def thresh_adaptive_gaussian(im):
    if not isinstance(im, np.ndarray):
        im = np.array(im)
        
    return cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
