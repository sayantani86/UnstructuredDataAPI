import pytesseract

def image_to_text(image):
    return pytesseract.image_to_string(image, config='--psm 6')