import cv2

def rotateImage(image):
    if not isinstance(image, np.ndarray):
        image = np.array(image)
        
    rows,cols = img.shape
    
    M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
    
    return cv2.warpAffine(img,M,(cols,rows))