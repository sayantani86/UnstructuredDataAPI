import numpy as np
import cv2

def thresh_binary(im, threshold=127):
    """Image has to be in gray scale.Single threshold value for entire image"""
    
    return cv2.threshold(im, threshold, 255, cv2.THRESH_BINARY)

def thresh_binary_inv(im, threshold=127):
    """Image has to be in gray scale"""
    
    return cv2.threshold(im, threshold, 255, cv2.THRESH_BINARY_INV)

def thresh_trunc(im, threshold=127):
    """Image has to be in gray scale"""
    
    return cv2.threshold(im, threshold, 255, cv2.THRESH_TRUNC)

def thresh_to_zero(im, threshold=127):
    """Image has to be in gray scale"""
    
    return cv2.threshold(im, threshold, 255, cv2.THRESH_TOZERO)

def thresh_to_zero_inv(im, threshold=127):
    """Image has to be in gray scale"""
    
    return cv2.threshold(im, threshold, 255, cv2.THRESH_TOZERO_INV)

def thresh_adaptive_mean(im):
    """Image has to be in gray scale"""
    
    return cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)

def thresh_adaptive_mean_inv(im):
    """Image has to be in gray scale"""
    
    return cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,11,2)

def thresh_adaptive_gaussian(im):
    """Image has to be in gray scale"""
    
    return cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,2)

def thresh_adaptive_gaussian_inv(im):
    """Image has to be in gray scale"""
    
    return cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11,2)

def thresh_otsu(im):
    """Image has to be in gray scale"""
    
    return cv2.threshold(im, 0,255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

def thresh_otsu_inv(im):
    """Image has to be in gray scale"""
    
    return cv2.threshold(im, 0,255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
