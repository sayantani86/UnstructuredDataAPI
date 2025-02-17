import numpy as np

def convert_BGR_to_GRAY(image):
    """Image load by opencv"""

    if not isinstance(image, np.ndarray):
        image = np.array(image)
        
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def convert_RGB_to_HSV(im):
    """Image load by PIL"""
    
    return im.convert('HSV')