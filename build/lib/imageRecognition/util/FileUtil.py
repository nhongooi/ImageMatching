import logging
from cv2 import imread


def open_img(path):
    """ Open an image given path

    Parameters
    -----------
    path: absolute path of the image

    Return
    -----------
    a PIL image"""

    try:
        image = imread(path)
    except IOError as e:
        logging.info("File not found", e, path)
        return None
    else:
        return image

# TODO find a good way to find if a picture is colored
def iscolor(image):
    """ Check image if loaded as color or grey
        by identifying number of channel

        Returns
        ---------
        Boolean"""
    # color image has 3 channels, RGB.
    if image.shape[2] == 3:
        return True

    return False


def isAcceptableSize(image, blocksize):
    """ Check minimum dimension of image

        Parameters
        -----------
        blocksize - size of blocks in row and col of image
        image - PIL image

        Return
        -----------
        boolean if pass larger than 4x4"""
    height = len(image)
    width = len(image[1])
    if (width/blocksize) >= 2 and (height/blocksize) >= 2:
        return True
    return False
