import csv
from PIL import Image
import numpy as np
import random

from rando import get_random_image
from root import Root


class ImageCreator():
    def __init__(self):
        self.root = 'hasyv2/'

        self.d = dict()
        # load keys
        with open(self.root + 'symbols.csv') as f:
            reader = csv.reader(f, delimiter=',', quotechar='\"')
            for row in reader:
                if '{' in row[1] and '}' in row[1]:
                    while row[1][-1] != '{':
                        row[1] = row[1][:-1]
                self.d[row[1]] = []

        # load values
        with open(self.root + 'hasy-data-labels.csv') as f:
            reader = csv.reader(f, delimiter=',', quotechar='\"')
            for row in reader:
                if '{' in row[2] and '}' in row[2]:
                    while row[2][-1] != '{':
                        row[2] = row[2][:-1]
                self.d[row[2]].append(self.root + row[0])

    def move_bbox(self, bbox, x=0, y=0):
        """
        Shift part of formula, only bboxes

        Args:
            bbox (list): bbox to be shifted
            x (int): x offset
            y (int): y offset

        Returns:
            bbox: shifted bbox
        """

        new_bb = []

        for bb in bbox:
            e = bb['el']
            b = []
            for d in bb['bbox']:
                new_x = d[0] + x
                new_y = d[1] + y
                b.append((new_x, new_y))

            new_bb.append({
                'el': e,
                'bbox': b
            })

        return new_bb

    def concat_images(self, im1, im2, bb1, bb2, d='h'):
        """
        Concatenate two images, horizontaly or verticaly, if its verticaly, images are centered

        Args:
            im1 (Image): fist image
            im2 (Image): second image
            bb1 (list): bbox of first image
            bb2 (list): bbox of second image
            d (string): direction of concatenation, h-horizontal, v-vertical
                Defaults to 'h'

        Returns:
            Image, bbox: concatenated image.
        """

        # concat images horizontaly
        if d == 'h':
            max_h = max(im1.height, im2.height)
            diff = abs(im1.height - im2.height)

            cnt = Image.new('RGBA', (im1.width + im2.width, max_h), color=(255, 255, 255, 0))
            if im1.height > im2.height:
                cnt.paste(im1, (0, 0))
                cnt.paste(im2, (im1.width, diff))
                bb2 = self.move_bbox(bb2, y=diff)
            else:
                cnt.paste(im1, (0, diff))
                cnt.paste(im2, (im1.width, 0))
                bb1 = self.move_bbox(bb1, y=diff)

            bb1 += bb2
            return cnt, bb1


        return None, None
    
    ## BBOX (BOTTOM LEFT, BOTTOM RIGHT, TOP RIGHT, TOP LEFT)
    def bbox_of_image(self, prev, image):
        """
        Returns the bounding box of new image in relations to the previous image
        
        Args:
            prev: bbox of previous element
            image: image that we want to find the bbox for

        Returns:
            list: bbox
        """

        start = prev[1]

        dims = image.size

        bbox = [
            (start),
            (start[0] + dims[0], start[1]),
            (start[0] + dims[0], start[1] + dims[1]),
            (start[0], start[1] + dims[1])
        ]

        return bbox

    def parse_formula(self, formula):
        """
        Preprocesing formula before creating image.

        Args:
            formula (string): latex formula
        
        Returns:
            array of latex elements
        """

        formula = list(formula)

        f = []
        s = ''

        for e in formula:
            s += e
            if s in self.d.keys() or s in ['}', '(', ')']:
                f.append(s)
                s = ''

        return f

    def get_dist(self, bb):
        """
        Get dimentsions for root or fraction

        Args:
            bb: bboxes of all elements under the root
        """

        # get max height
        m = 0
        for el in bb:
            e = el['bbox'][-1][1]
            if e > m:
                m = e

        # get length
        first = bb[0]['bbox'][-1]
        last = bb[-1]['bbox'][-1]
        dif = last[0] - first[0]
        return (dif, m)

    def create_image(self, formula, start=[(0, 0), (0, 0), (0, 0), (0, 0)]):
        """
        Creates image with different letters each time

        Args:
            formula (string): latex formula

        Returns:
            Tuple (image, bbox)
                where bbox is a list of dicts with class and bbox of each element
        """

        # initialize image
        parts = []
        parts.append({"bbox": start, "el": "START/000"})
        image = Image.new('RGBA', (0, start[2][1]), color='white')

        formula = self.parse_formula(formula)

        i = 0
        while i < len(formula):
            if formula[i] == '\\sqrt{':
                # create root
                r = get_random_image(formula[i], self.d)
                root = Root(r)
                under = ''
                i += 1
                # get formula under the root
                while formula[i] != '}':
                    under += formula[i]
                    i += 1
                i += 1
                # Get image under the root
                ur, bb = self.create_image(under, parts[-1]['bbox'])

                # put root and image together
                size = self.get_dist(bb)
                root.create_root(size, parts[-1]['bbox'])
                img, bb = root.insert_image(ur, bb)
                image, parts = self.concat_images(image, img, parts, bb)
            else:
                # get new element and add its bbox
                new_image = get_random_image(formula[i], self.d)
                bbox = self.bbox_of_image(parts[-1]['bbox'], new_image)
                bb = [{
                    "bbox": bbox,
                    "el": formula[i]
                }]
                image, parts = self.concat_images(image, new_image, parts, bb)
                i += 1
        
        return image, parts


if __name__ == '__main__':
    creator = ImageCreator()
    img, p = creator.create_image("2288-5-(6+8)-\\sqrt{2+3}")
    img.show()
    print(p)