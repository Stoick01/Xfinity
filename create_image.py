import csv
from PIL import Image
import numpy as np
import random

from rando import get_random_image
from root import Root
from fraction import Fraction


class ImageCreator():
    """
    Creates single image and bbox
    """

    def __init__(self):
        self.root = 'hasyv2/'
        self.root_ind = 1

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

    def concat_images(self, im1, im2, bb1, bb2, d='h', center_v=False):
        """
        Concatenate two images, horizontaly or verticaly, if its verticaly, images are centered

        Args:
            im1 (Image): fist image
            im2 (Image): second image
            bb1 (list): bbox of first image
            bb2 (list): bbox of second image
            d (string): direction of concatenation, h-horizontal, v-vertical
                Defaults to 'h'
            center_v (bool): declares if image should be ceneterd vertically instead shifted

        Returns:
            Image, bbox: concatenated image.
        """

        # concat images horizontaly
        if d == 'h':
            max_h = max(im1.height, im2.height)
            diff = abs(im1.height - im2.height)

            x_shift = random.randint(1, 5)

            cnt = Image.new('RGBA', (im1.width + im2.width + x_shift, max_h), color=(255, 255, 255, 0))
            if im1.height > im2.height:
                cnt.paste(im1, (0, 0))
                cnt.paste(im2, (im1.width + x_shift, diff // 2))
                bb2 = self.move_bbox(bb2, y=diff // 2)
            else:
                cnt.paste(im1, (0, diff // 2))
                cnt.paste(im2, (im1.width + x_shift, 0))
                bb1 = self.move_bbox(bb1, y=diff // 2)

            bb2 = self.move_bbox(bb2, x=x_shift)

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
            (start[0], 0),
            (start[0] + dims[0], 0),
            (start[0] + dims[0], dims[1]),
            (start[0], dims[1])
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
            if s in self.d.keys() or s in ['{', '}', '(', ')'] or s == '\\frac{':
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

        # x_min = bb[0]['bbox'][-1][0]
        # x_max = bb[-1]['bbox'][-1]

        # get length
        first = bb[0]['bbox'][-1]
        last = bb[-1]['bbox'][2]
        dif = last[0] - first[0]
        return (dif, m)

    def get_formula_part(self, formula, idx):
        """
        Function to get part of the formula within the {}, for example under the root, or in fraction

        Args:
            formula: formula we are parsing
            idx: start index

        Returns:
            Tuple (string, int): returns formula and end index
        """

        # init part of formula, and get 
        part = ''
        opened = 1

        while True:
            if formula[idx] == '}':
                opened -= 1
            elif '{' in formula[idx]:
                opened += 1
            if opened == 0:
                idx += 1
                break
            part += formula[idx]
            idx += 1

        return part, idx

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
        image = Image.new('RGBA', (0, start[2][1]), color=(255, 255, 255, 0))

        formula = self.parse_formula(formula)

        i = 0
        while i < len(formula):
            if formula[i] == '\\sqrt{':
                # create root
                r = get_random_image(formula[i], self.d)
                root = Root(r)
                
                # get formula under the root
                i += 1
                under, i = self.get_formula_part(formula, i)

                # Get image under the root
                ur, bb = self.create_image(under, parts[-1]['bbox'])

                # put root and image together
                size = self.get_dist(bb)
                root.create_root(size, parts[-1]['bbox'])
                img, bb = root.insert_image(ur, bb, self.root_ind)
                self.root_ind += 1
                image, parts = self.concat_images(image, img, parts, bb)
            elif formula[i] == '\\frac{':
                # get numerator
                i += 1
                numer, i = self.get_formula_part(formula, i)

                numer_img, numer_bb = self.create_image(numer, parts[-1]['bbox'])

                # get denuminator
                i += 1
                denum, i = self.get_formula_part(formula, i)

                denum_img, denum_bb = self.create_image(denum, parts[-1]['bbox'])

                # create fraction
                size_numer = self.get_dist(numer_bb)
                size_denum = self.get_dist(denum_bb)

                size = max(size_numer, size_denum)

                fraction = Fraction()

                fraction.create_fraction(size, parts[-1]['bbox'])
                img, bb = fraction.insert_num_denum(numer_img, denum_img, numer_bb, denum_bb)

                image, parts = self.concat_images(image, img, parts, bb, center_v=True)
            else:
                # get new element and add its bbox
                new_image = get_random_image(formula[i], self.d)
                bbox = self.bbox_of_image(parts[-1]['bbox'], new_image)
                bb = [{
                    "bbox": bbox,
                    "el": formula[i]
                }]
                c_v = False
                if formula[i] in ['+', '-', '*', '/']:
                    c_v = True
                image, parts = self.concat_images(image, new_image, parts, bb, center_v=c_v)
                i += 1

        return image, parts

    def generate(self, formula, background_color=None, dims=None):
        """
        Generate image with background

        Args:
            formula: latex formula
            background_color: background color
            padding: if true add padding to image

        Returns:
            Tuple: image, bbox
        """

        image, bbox = self.create_image(formula)

        image, bbox = self.add_padding(image, bbox, dims)

        image = self.fill_background(image, background_color)

        return image, bbox

    def add_padding(self, image, bbox, dims=None):
        """
        Add random padding to all the sides of the image

        Args:
            image: pil rgba image
            bbox: bbox off the image

        Returns:
            Tuple (image, bbox): 
        """

        max_x = 64
        max_y = 32

        if dims != None:
            max_x = dims[0] - image.width
            max_y = dims[1] - image.height

        offset_x = random.randint(0, max_x)
        offset_y = random.randint(0, max_y)

        new_image = Image.new('RGBA', (image.width + max_x, image.height + max_y), color=(255, 255, 255, 0))
        new_image.paste(image, (offset_x, offset_y))

        bbox = self.move_bbox(bbox, x=offset_x, y=offset_y)

        return new_image, bbox


    def fill_background(self, img, color=None):
        """
        Fill background of rgba image, and convert it to rgb

        Args:
            image: rgba image
            color: backcolor is set to random shade of white (gray) if no color is provided

        Returns:
            Image: PIL image object
        """

        if color == None:
            colors = ['#fff', '#eee', '#ddd', '#ccc', '#bbb', '#aaa', '#999', '#888']
            color = random.choice(colors)

        back = Image.new('RGB', img.size, color)
        back.paste(img, mask=img.split()[3])

        return back


if __name__ == '__main__':
    creator = ImageCreator()
    img, p = creator.create_image("2288-5-(6+8)-\\sqrt{2+\\sqrt{3+4}}")
    img.show()
    print(p)