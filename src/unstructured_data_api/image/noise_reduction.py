import numpy as np
import cv2

def average_blur(img, kernel_size=(5, 5)):
    """It replaces each pixel's value with the average of its neighboring pixel values within the kernel size"""
    
    if not isinstance(img, np.ndarray):
        img = np.array(img)
        
    return cv2.blur(img, kernel_size) 

def gaussian_blur(img, kernel_size=(5, 5)):
    """It uses a Gaussian function (bell-shaped curve) to calculate the weights for the neighboring pixels.Pixels closer to the center have higher weights, resulting in a more natural blur"""
    
    if not isinstance(img, np.ndarray):
        img = np.array(img)
        
    return cv2.GaussianBlur(img, kernel_size, 0) 

def median_blur(img, kernel_size=5):
    """Replaces each pixel's value with the median value of its neighbors"""

    if not isinstance(img, np.ndarray):
        img = np.array(img)
    
    return cv2.medianBlur(img, kernel_size) 

def bilateral_filter(img):
    """It's an edge-preserving blurring technique. It applies a Gaussian filter in both the spatial domain and the intensity domain. This means that it considers both the distance between pixels and their color difference, preserving sharp edges while smoothing the rest of the image"""
    
    if not isinstance(img, np.ndarray):
        img = np.array(img)
    
    return cv2.bilateralFilter(img, 9, 75, 75)

def motion_blur(img):
    if not isinstance(img, np.ndarray):
        img = np.array(img)
        
    kernel = np.zeros((11, 11))
    kernel[:, 5] = np.ones(11)
    kernel /= 11
    return cv2.filter2D(img, -1, kernel)

