import tarfile
import os
import shutil


if __name__ == '__main__':
    print('Extracting files...')
    if os.path.exists('HASYv2.tar.bz2'):
        tar = tarfile.open('HASYv2.tar.bz2', 'r:bz2')
        tar.extractall('hasyv2')
        tar.close()

        print('Cleaning up...')
        shutil.rmtree('hasyv2')
    else:
        print('Unable to find original dataset...')
