import os
import numpy as np
from PIL import Image

def save_image(image, filename):
    image = Image.fromarray( (255*image).astype(np.uint8) )
    image.save(filename)
