from PIL import ImageDraw, Image
from datetime import datetime
import random

from create_image import ImageCreator

if __name__ == '__main__':
    creator = ImageCreator()
    # img, p = creator.generate("2288-5-(6+8)-\\sqrt{2}")
    # img, p = creator.generate("2288-5-(6+8)-\\sqrt{2+\\sqrt{3+4}}")
    # img, p = creator.generate("2288-5-(6+8)-\\sqrt{\\frac{2}{4+8}}")

    img, p = creator.generate("45\\cdot(6+8)-\\sqrt{2+\\sqrt{3+4}}", background_color='#fff')

    im = ImageDraw.Draw(img)

    for bb in p:
        b = bb['bbox']
        if bb['el'] == 'START/000':
            continue

        random.seed(datetime.now())
        color = "#%06x" % random.randint(0x555555, 0xAAAAAA)

        im.rectangle([b[0], b[2]], outline=color)

    img.show()