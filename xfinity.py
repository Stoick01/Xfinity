import tarfile
import os
import shutil
import sys
import string

from dataset import Dataset

if __name__ == '__main__':
    # print('Extracting files...')
    # if os.path.exists('HASYv2.tar.bz2'):
    #     tar = tarfile.open('HASYv2.tar.bz2', 'r:bz2')
    #     tar.extractall('hasyv2')
    #     tar.close()

    #     print('Cleaning up...')
    #     shutil.rmtree('hasyv2')
    # else:
    #     print('Unable to find original dataset...')
    #     exit()

    idx = 1

    dims = None
    color = None
    size = 1
    formulas = []
    path = 'dataset'

    if sys.argv[idx] == '--help':
        print('')
        print('Usage:')
        print('  python xfinity.py <command> [options]')

        print('')
        print('General Options:')
        options = [
            ['--help', 'Show help'],
            ['--dims <width>x<height>', 'Generate images with specified width and height (ex. 260x48)'],
            ['--color <color>', 'Sets background color, same for all the images, note color must be hex number'],
            ['--size <size>', 'Defines number of train images created for each formula provided'],
            ['--path <path>', 'Path where you want to save the dataset to'],
            ['--formula [formulas]', 'Provide list of formulas you want to create datasets from'],
        ]

        for o in options:
            print('  {:25} {}'.format(o[0], o[1]))
        exit()

    if idx < len(sys.argv) and sys.argv[idx] == '--dims':
        idx += 1
        if idx >= len(sys.argv):
            print('Dimensions are not provided')
            exit()

        if 'x' not in sys.argv[idx]:
            print('Argument --dims is not of the correct format, try something like 360x280')
            exit()

        d = sys.argv[idx].split('x')

        if not d[0].isdigit() or not d[1].isdigit():
            print('One of the arguments provided in --dims is not a number')
            exit()

        dims = []

        dims.append(int(d[0]))
        dims.append(int(d[1]))

        idx += 1

    if idx < len(sys.argv) and sys.argv[idx] == '--color':
        idx += 1
        if idx >= len(sys.argv):
            print('Color is not provided')
            exit()

        c = sys.argv[idx]

        if not c.startswith('#') or (len(c) != 4 and len(c) != 7) or not all(s in string.hexdigits for s in c[1:]):
            print("Color in --color argument is not hexadecimal value")
            exit()

        color = c
        idx += 1

    if idx < len(sys.argv) and sys.argv[idx] == '--size':
        idx += 1
        if idx >= len(sys.argv):
            print('Size is not provided')
            exit()

        if not sys.argv[idx].isdigit():
            print('Size in the argument --size is not a number.')
            exit()

        size = int(sys.argv[idx])
        idx += 1

    if idx < len(sys.argv) and sys.argv[idx] == '--path':
        idx += 1
        if idx >= len(sys.argv):
            print('Path is not provided')
            exit()

        if not os.path.exists(sys.argv[idx]):
            print('Path does not exist')
            exit()

        path = sys.argv[idx]
        idx += 1

    if idx < len(sys.argv) and sys.argv[idx] == '--formulas':
        idx += 1
        if idx >= len(sys.argv):
            print('0 formulas provided')
            exit()

        while idx < len(sys.argv):
            formulas.append(sys.argv[idx])
            idx += 1


    dataset = Dataset(dims, color, size, path, formulas)
    dataset.generate()