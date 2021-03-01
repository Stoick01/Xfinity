import os
import shutil

from PIL import Image

from create_image import ImageCreator
from bbox import BboxCreator

class Dataset():
    """
    Used to create full dataset.
    """

    def __init__(self, dims, color, size, path, formulas):
        self.dims = dims
        self.color = color
        self.train_size = size
        self.test_size = int(size * 0.2)

        self.path = path
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)

        self.formulas = formulas

        self.image_creator = ImageCreator()

    def generate(self):
        """
        Generates the dataset
        """

        # create train and test directory
        train_path = os.path.join(self.path, 'train')
        test_path = os.path.join(self.path, 'test')

        if os.path.exists(train_path):
            shutil.rmtree(train_path)

        if os.path.exists(test_path):
            shutil.rmtree(test_path)

        os.mkdir(train_path)
        os.mkdir(test_path)

        for formula in self.formulas:

            # create test images
            loc = os.path.join(train_path, formula)
            os.mkdir(loc)

            for i in range(self.train_size):
                image, bbox = self.image_creator.generate(formula, background_color=self.color, dims=self.dims)
                filename = str(i) + '.jpg'

                image.save(os.path.join(loc, filename), 'JPEG')
                print(f'Train {formula}, {i+1:>{len(str(self.train_size))}}/{self.train_size}', end='\r')

                bb_creator = BboxCreator(formula, filename)
                bb_creator.create_file(loc, bbox)
            print('')


            # create train images
            loc = os.path.join(test_path, formula)
            os.mkdir(loc)

            for i in range(self.test_size):
                image, bbox = self.image_creator.generate(formula, background_color=self.color, dims=self.dims)
                filename = str(i) + '.jpg'

                image.save(os.path.join(loc, filename), 'JPEG')
                print(f'Test {formula}, {i+1:>{len(str(self.test_size))}}/{self.test_size}', end='\r')

                bb_creator = BboxCreator(formula, filename)
                bb_creator.create_file(loc, bbox)
            print('')
