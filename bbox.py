import os

class BboxCreator():
    def __init__(self, formula, filename):
        self.formula = formula
        self.filename = filename

        self.pre_objs = []
        self.objs = []
        self.after_objs = []

        self.pre_objs.append('<annotation>')
        self.pre_objs.append(f'\t<formula>{formula}</formula>')
        self.pre_objs.append(f'\t<filename>{filename}</filename>')
        self.pre_objs.append('')
        self.pre_objs.append('\t<objects>')

        self.after_objs.append('\t</objects>')
        self.after_objs.append('</annotation>')


    def create_file(self, loc, bbox):
        """
        Creates the bbox file for image
        
        Args:
            loc: path where to save the file
            bbox: bbox of an image
        """
        for b in bbox:
            name = b['el']
            if name == 'START/000':
                continue
        
            bb = b['bbox']

            xmin, ymin = bb[0]
            xmax, ymax = bb[2]

            self.append_object(name, xmin, xmax, ymin, ymax)

        self.write_out(loc)


    def append_object(self, name, xmin, xmax, ymin, ymax):
        """
        Appends the object to output file

        Args:
            name: name of object
            xmin, xmax, ymin, ymax: locations of an object
        """
        
        self.objs.append('\t\t<object>')
        self.objs.append(f'\t\t\t<name>{name}</name>')
        self.objs.append('\t\t\t<bbox>')
        self.objs.append(f'\t\t\t\t<xmin>{xmin}</xmin>')
        self.objs.append(f'\t\t\t\t<ymin>{ymin}</ymin>')
        self.objs.append(f'\t\t\t\t<xmax>{xmax}</xmax>')
        self.objs.append(f'\t\t\t\t<ymax>{ymax}</ymax>')
        self.objs.append('\t\t\t</bbox>')
        self.objs.append('\t\t</object>')

    def write_out(self, loc):
        """
        Creates the file

        Args:
            loc: path to the file
        """

        fl = self.filename.split('.')[0] + '.xml'
        
        path = os.path.join(loc, fl)

        with open(path, 'w') as f:
            for l in self.pre_objs:
                f.write(l + '\n')

            for l in self.objs:
                f.write(l + '\n')

            for l in self.after_objs:
                f.write(l + '\n')