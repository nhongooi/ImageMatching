from cv2 import imread


def size_checker(blocksize, image):
    """ Check minimum dimension of image

        Parameters
        -----------
        blocksize - size of blocks in row and col of image
        image - PIL image

        Return
        -----------
        boolean if pass larger than 4x4"""
    width, height = image.size

    if (width/blocksize) >= 4 and (height/blocksize) >= 4:
        return True
    return False


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
    except OSError:
        print("Given file is not an image file")
    else:
        return image


def iscolor(image):
    """ Check image if loaded as color or grey
        by identifying number of channel

        Returns
        ---------
        Boolean"""
    # color image has 3 channels, RGB.
    if len(image[1, 1]) == 3:
        return True

    return False
