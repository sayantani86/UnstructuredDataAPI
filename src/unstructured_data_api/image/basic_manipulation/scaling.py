import numpy as np
import cv2

def shrink_image(img):
    return cv2.resize(img, None, fx=2, fy=2, interpolation = cv2.INTER_AREA)

def resize(img):
    return cv2.resize(img, None, fx=2, fy=2, interpolation = cv2.INTER_CUBIC)

def zoom_image(img):
    height, width = img.shape[:2]
    
    return cv2.resize(img, (2*width, 2*height), interpolation = cv2.INTER_LINEAR)

def shift_img(img, tx, ty):
    rows,cols = img.shape
    
    M = np.float32([[1,0,tx],[0,1,ty]])
    
    return cv2.warpAffine(img,M,(cols,rows))

def rotate_img(img):
    rows,cols = img.shape
    
    M = cv.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0),90,1)
    dst = cv.warpAffine(img,M,(cols,rows))
    
    return dst

