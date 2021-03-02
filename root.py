import csv
from PIL import Image, ImageDraw
import numpy as np
import random
from datetime import datetime
import time
from rando import get_random_image, convert_to_transparent

class Root():
    def __init__(self, img):
        self.img = img
        self.arr = None
        self.offset = 0

    def find_tail(self):
        """
        Finds the last pixels of the root, so that it can extend it to fit the math expression
        """
        ## Get the tail of squared root
        for k in range(32):
            a = np.array(self.img)[:, -k]

            found = False
            cnt = len(np.where((a == (0, 0, 0, 255)).all(axis=1))[0])
            if cnt != 2:
                continue

            b = np.array(self.img)[:, -(k+1)]
            a_s = np.where((a == (0, 0, 0, 255)).all(axis=1))[0].sum()
            b_s = np.where((b == (0, 0, 0, 255)).all(axis=1))[0].sum()

            if abs(a_s- b_s) > 4:
                continue

            self.arr = a  
            self.offset = k
            break

    def create_root(self, size, start):
        """
        Creates the root, with specified size
        Args:
            size (int, int): width and height of an area under the root
            start (list): bbox of element before root
        Returns:
            Image: 
        """
        self.find_tail()

        width = size[0]
        full = Image.new('RGBA', (width, 36), color=(255, 255, 255, 0))
        offset_y = 4
        base = 4
        offs = [-1, 0, 1]
        cnt = 25

        # Create root image
        full.paste(self.img, (0, 4))
        o = 0
        im = Image.fromarray(self.arr)
        im = convert_to_transparent(im)

        for i in range(width - 32 + self.offset):
            if cnt == 0:
                o = random.choice(offs)
                while abs(base - offset_y - o) > 2:
                    random.seed(datetime.utcnow())
                    o = random.choice(offs)
                offset_y += o
                cnt = 25
            cnt -= 1
            full.paste(im, (32 + i - self.offset, offset_y))

        # resize root and get its bbox
        full = full.resize((size[0], size[1]), Image.ANTIALIAS)
        dims = self.get_bbox(full, start[1])
        self.bbox = dims
        self.root = full
        return full, dims

    def get_bbox(self, image, start):
        """
        Get bbox of root

        Args:  
            image: root image
            start: start index

        Returns:
            list: bbox of root
        """

        x_start = 0 + start[0]
        x_end = image.size[0] + start[0]

        y_start = 0
        y_end = start[1]

        img = np.array(image)

        # find start index
        for i in range(len(img)):
            if any(np.equal(img[i], [0, 0, 0, 255]).all(1)):
                y_start += i
                break

        # find end index
        for i in reversed(range(len(img))):
            if any(np.equal(img[i], [0, 0, 0, 255]).all(1)):
                y_end += i
                break

        self.offset_y = y_start

        # put all together
        bbox = [
            (x_start, y_start - self.offset_y//2),
            (x_end, y_start - self.offset_y//2),
            (x_end, y_end - self.offset_y//2),
            (x_start, y_end - self.offset_y//2)
        ]

        return bbox


    def shift_formula(self, bbox, root_off, ind):
        """
        Shifts all the elements that under the root, to their relative location.

        Args:
            bbox (list): list of bboxes for each element under the root
            image_size (tuple): coordinates of the start index

        Returns:
            list: bbox shifted for under root
        """

        x = 32-self.offset-15
        y = 10

        new_bb = []

        for bb in bbox:
            e = bb['el']
            b = []
            bbo = bb['bbox']
            xmin, ymin = bbo[0]
            xmax, ymax = bbo[2]
            xmin += x
            ymin += y
            xmax += x
            ymax += y

            b.append((xmin, ymin))
            b.append((xmax, ymin))
            b.append((xmax, ymax))
            b.append((xmin, ymax))
            
            # for d in bb['bbox']:
            #     new_x = d[0] + x
            #     new_y = d[1] + y
            #     b.append((new_x, new_y))

            new_bb.append({
                'el': e,
                'bbox': b
            })

        bn = []
        for b in self.bbox:
            bx = b[0]
            by = b[1] + 5*ind - root_off
            bn.append((bx, by))
        self.bbox = bn
        
        # add roots bbox
        new_bb += [{
            'bbox': self.bbox,
            'el': '\\sqrt{'
        }]

        return new_bb

    def insert_image(self, im, bbox, ind):
        """
        Inserts formula under the root
        
        Args:
            im (Image): image of formula that goes under the root
            root (Image): root image

        Returns:
            Tuple: image and bbox
        """

        # fit image under the root
        self.new_size = (im.width, self.root.height - self.offset_y - 5)
        # im = im.resize(self.new_size, Image.ANTIALIAS)
        
        # concat root and formula under it
        max_h = max(im.height, self.root.height)
        cnt = Image.new('RGBA', (self.root.width, max_h+self.offset_y+20), color=(255, 255, 255, 0))
        cnt.paste(self.root, (0, self.offset_y//2+5*ind - im.height//32))
        cnt.paste(im, (32-self.offset-15, self.offset_y+10), im)

        bbox = self.shift_formula(bbox, im.height//32, ind)

        cnt = cnt.crop((0, self.offset_y, cnt.width, cnt.height))

        return cnt, bbox
