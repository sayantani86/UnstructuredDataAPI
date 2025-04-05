def getParas(image_text):
    return image_text.split('\n+')

def getSents(image_text):
    return image_text.split('\n')