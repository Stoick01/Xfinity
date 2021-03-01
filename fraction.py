import random
from datetime import datetime

from PIL import Image
import numpy as np

from rando import convert_to_transparent

class Fraction():

    def get_bbox(self, size, start):
        """
        Generates the bbox of the root line

        Args:
            size: size of fraction
            start: start of the bbox

        Retursn:
            list: bbox of root line
        """

        width = size[0]
        height = 6

        start = start[2]

        bbox = [
            (start[0], 0),
            (start[0] + width, 0),
            (start[0] + width, height),
            (start[0], height)
        ]

        return bbox



    def create_fraction(self, size, start):
        """
        Create fraction

        Args:
            size: dimensions of fraction
            start: start location

        Returns:
            Tuple (Image, list): returns image of fraction and bboxes
        """

        full = Image.new('RGBA', (size[0], 6), color=(255, 255, 255, 0))

        off = 0
        offs = [-1, 0, 1]
        cnt = 25
        img = np.array([
            [255, 255, 255, 0],
            [255, 255, 255, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [255, 255, 255, 0],
            [255, 255, 255, 0],
        ], dtype=np.uint8)

        img = Image.fromarray(img)
        img = convert_to_transparent(img)

        for i in range(size[0]):
            if cnt == 0:
                o = random.choice(offs)
                while abs(off + o) > 2:
                    random.seed(datetime.utcnow())
                    o = random.choice(offs)
                off += o
                cnt = 25
            full.paste(img, (i, off))
            cnt -= 1

        self.bbox = self.get_bbox(size, start)
        self.fraction = full

        return full, self.bbox

    def shift_formula(self, numer_bb, denum_bb, numer_offset, denum_offset, self_offset):
        """
        Shifts bboxes to fit the fraction

        Args:
            numer_bb: bbox of numerator
            denum_bb: bbox of denumerator
            numer_offset: offset of numerator
            denum_offset: offset of denumerator

        Returns:
            list: shifted bboxes plus fraction bbox
        """

        bbox = []

        for bb in numer_bb:
            e = bb['el']
            b = []
            for d in bb['bbox']:
                new_x = d[0] + numer_offset[0]
                new_y = d[1] + numer_offset[1]
                b.append((new_x, new_y))

            bbox.append({
                'el': e,
                'bbox': b
            })

        for bb in denum_bb:
            e = bb['el']
            b = []
            for d in bb['bbox']:
                new_x = d[0] + denum_offset[0]
                new_y = d[1] + denum_offset[1]
                b.append((new_x, new_y))

            bbox.append({
                'el': e,
                'bbox': b
            })

        bn = []
        for b in self.bbox:
            bx = b[0]
            by = b[1] + self_offset
            bn.append((bx, by))
        self.bbox = bn

        bbox += [{
            'el': '\\frac{',
            'bbox': self.bbox
        }]

        return bbox

    def find_denum_start(self, denum):
        """
        Find start off the denuminator.

        Args:
            denum: denum image

        Returns:
            int: y_offset
        """
        y_start = 0
        denum = np.array(denum)

        for i in range(len(denum)):
            if any(np.equal(denum[i], [0, 0, 0, 255]).all(1)):
                y_start += i
                break

        return y_start

    def insert_num_denum(self, numer_img, denum_img, numer_bb, denum_bb):
        """
        Insert numerator and denumeratro into the fraction and shift bboxes

        Args:
            numer_img: Image of numerator
            denum_img: Image of denumerator
            numer_bb: bbox of numerator
            denum_bb: bbox of denumerator

        Returns:
            Tuple (Image, list): Retursn completete fraction and bbox
        """

        d_off = self.find_denum_start(denum_img) // 2

        new_size = (self.fraction.width, numer_img.height + denum_img.height + self.fraction.height - d_off)

        cnt = Image.new('RGBA', new_size, color=(255, 255, 255, 0))

        numer_offset = [0, 0]
        denum_offset = [0, numer_img.height + self.fraction.height - d_off]

        if numer_img.width > denum_img.width:
            denum_offset[0] = (numer_img.width - denum_img.width) // 2
        else:
            numer_offset[0] = (denum_img.width - numer_img.width) // 2

        cnt.paste(denum_img, denum_offset)
        cnt.paste(numer_img, numer_offset)
        cnt.paste(self.fraction, (0, numer_img.height))

        bbox = self.shift_formula(numer_bb, denum_bb, numer_offset, denum_offset, numer_img.height)

        return cnt, bbox