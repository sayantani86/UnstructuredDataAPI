import numpy as np

def get_dimensions(im):
    if not isinstance(im, np.ndarray):
        im = np.array(im)
        
    return im.shape

def square_resize(im):
    height, width = get_dimensions(im)
    
    size = min (height, width)
    left = (width - size) / 2
    top = (height - size) / 2
    right = (width + size) / 2
    bottom = (height + size) / 2
    cropped = im.crop((left, top, right, bottom))
    
    return cropped

def crop_by_default_thresh(image):
    if not isinstance(image, np.ndarray):
        image = np.array(image)
        
    image_cropped=None
    
    h,w=image.shape[:2]
    image_cropped=image[50:h-100,50:w-50:]
    
    return image_cropped

def crop_with_size(image,height,width):
    if not isinstance(image, np.ndarray):
        image = np.array(image)
        
    image_cropped=None
    
    h,w=image.shape[:2]
    image_cropped=image[height:h-height,width:w-width:]
    
    return image_cropped
