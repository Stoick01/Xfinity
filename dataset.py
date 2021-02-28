from create_image import ImageCreator

class Dataset():
    """
    Used to create full dataset.
    """

    def __init__(self, dims, color, size, dest, formulas):
        self.dims = dims
        self.color = color
        self.train_size = size
        self.test_size = int(size * 0.2)
        self.dest = dest
        self.formulas = formulas

        self.image_creator = ImageCreator()

    def generate(self):
        """"""
