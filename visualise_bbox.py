from PIL import ImageDraw
from datetime import datetime
import random

from create_image import ImageCreator

if __name__ == '__main__':
    creator = ImageCreator()
    # img, p = creator.create_image("2288-5-(6+8)-\\sqrt{2}")
    # img, p = creator.create_image("2288-5-(6+8)-\\sqrt{2+\\sqrt{3+4}}")

    img, p = creator.create_image("2288-5-(6+8)-\\frac{2}{4+8}")

    im = ImageDraw.Draw(img)

    for bb in p:
        b = bb['bbox']
        if bb['el'] == 'START/000':
            continue

        random.seed(datetime.now())
        color = "#%06x" % random.randint(0x555555, 0xAAAAAA)

        im.rectangle([b[0], b[2]], outline=color)

    img.show()