import random
from PIL import Image
from datetime import datetime
import numpy as np

def convert_to_transparent(image):
    """
    Converts white background to transparent

    Args:
        image: pillow RGB image

    Returns:
        image: RGBA transparent image
    """

    x = np.asarray(image.convert('RGBA')).copy()

    x[:, :, 3] = (255 - x[:, :, :3].mean(axis=2)).astype(np.uint8)

    return Image.fromarray(x)

def get_random_image(key, d):
    """
    Get random image for specified math simbol

    Args:
        key (string): element (ex. 2, 3, 4)
        d: dict of keys and image paths

    Returns:
        image
    """

    random.seed(datetime.now())
    if key == '(':
        images = d['\\circ']
        image = random.choice(images)
        image = Image.open(image)
        image = image.crop((0, 0, 12, 32))
    elif key == ')':
        images = d['\\circ']
        image = random.choice(images)
        image = Image.open(image)
        image = image.crop((16, 0, 32, 32))
    else:
        images = d[key]
        image = random.choice(images)
        image = Image.open(image)

    if key in ['+', '-', '/', '*']:
        image = image.resize((20, 20))

    return convert_to_transparent(image)