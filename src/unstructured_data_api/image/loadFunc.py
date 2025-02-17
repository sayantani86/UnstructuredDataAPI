from os import path, makedirs
from pdf2image import convert_from_path, convert_from_bytes
import cv2
from PIL import Image

def loadPDF(path_or_bytes, output_folder=None):
    if not path.exists(output_folder):
        makedirs(output_folder)
    
    images = []
    
    try:
        images = convert_from_bytes(open(path_or_bytes, "rb").read(), grayscale=True, use_pdftocairo=True, output_folder=output_folder)
    except Exception as e:
        images = convert_from_path(path_or_bytes, grayscale=True, use_pdftocairo=True, output_folder=output_folder)
            
    return images

def loadWithOpenCV(image_path):
    """Load image as numpy array.The image is in the BGR color space"""
    
    return cv2.imread(image_path)

def loadWithPIL(image_path):
    """Image is in RGB color space"""
    
    try:
        with Image.open(image_path) as img:
            img.load()
            
            return img
    except IOError:
        print("An error occurred while trying to open the image.")
