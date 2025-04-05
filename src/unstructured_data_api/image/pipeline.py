import cv2

from unstructured_data_api.image.loadFunc import *
from unstructured_data_api.image.basic_manipulation import *
from unstructured_data_api.image.smoothing import *
from unstructured_data_api.image.contour import *
from unstructured_data_api.image.morphology import *
from unstructured_data_api.image.thresholding import *

def addHorizontalContours(original):
    src = np.copy(original)
    
    gray = cv2.bitwise_not(original)

    gray = thresh_adaptive_mean(gray)
    
    horizontal = np.copy(gray)
    rows, cols = horizontal.shape
    
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (cols // 30, 1))
    horizontal = cv2.erode(horizontal, horizontalStructure)
    horizontal = cv2.dilate(horizontal, horizontalStructure)
    edges = thresh_adaptive_mean(horizontal)
    edges = cv2.bitwise_not(edges)
    
    kernel = np.ones((2, 2), np.uint8)
    edges = cv2.dilate(edges, kernel)
    
    (rows, cols) = np.where(edges != 0)

    smooth = cv2.blur(horizontal, (2, 2))
    horizontal[rows, cols] = smooth[rows, cols]
    
    contours, hierarchy = cv2.findContours(horizontal, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    boundRect = [None]*len(contours)

    for i, c in enumerate(contours):
        boundRect[i] = cv2.boundingRect(c)

    drawing = np.zeros((original.shape[0], original.shape[1], 3), dtype=np.uint8)

    for i in range(len(contours)):
        cv2.drawContours(src, contours, i, (0, 255, 0))
    
    return src, boundRect

def extractFormFields(image, boundRect):
    pass


