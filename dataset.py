import os
import shutil

from PIL import Image

from create_image import ImageCreator

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
                image, bbox = self.image_creator.generate(formula)
                filename = str(i) + '.jpg'

                image.save(os.path.join(loc, filename), 'JPEG')


            # create train images
            loc = os.path.join(test_path, formula)
            os.mkdir(loc)

            for i in range(self.test_size):
                image, bbox = self.image_creator.generate(formula)
                filename = str(i) + '.jpg'

                image.save(os.path.join(loc, filename), 'JPEG')
