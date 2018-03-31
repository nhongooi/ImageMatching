
import numpy as np
from imageRecognition.util.FileUtil import iscolor, size_checker
from imageRecognition.util.errors import DifferentBlockCountError, NullImageError, TooSmallImageError

def blockify(image, block_count=16):
    """ Divide image into blocks x blocks matrix,
        each block pieces of the image and average
        each channel for each block

        Parameters
        ---------------
        image : opencv image as numpy array
        block_count: number of x blocks horizontally and vertically
                block is only valid if it is at least 4x4 pixel

        Returns
        ----------------
        1D array of averaged blocks"""
    if image is None:
        raise NullImageError
    if size_checker(image, block_count) is False:
        raise TooSmallImageError

    image_avg = []
    height = image.shape[0] // block_count
    width = image.shape[1] // block_count

    for row in range(block_count):
        upper = row * height
        for col in range(block_count):
            left = col * width
            if row == (block_count-1) and col == (block_count-1):
                lower = image.shape[0]
                right = image.shape[1]
            elif col == (block_count-1):
                lower = (row+1) * height
                right = image.shape[1]
            elif row == (block_count-1):
                lower = image.shape[0]
                right = (col+1) * width
            else:
                lower = (row+1) * height
                right = (col+1) * width

            image_block = image[upper:lower, left : right]
            image_avg.append(avg_block(image_block))
    return image_avg


def avg_block(image):
    """ Calculate the average of each channel in
        the image

        Parameters
        -------------
        image - a block from original image or the original images

        Returns
        ----------
        tuple containing the averaged channels"""

    if iscolor(image) is True:
        return __avg_color(image)

    return __avg_grey(image)


def __avg_color(image):
    """ Average each channel in the image

        Returns
        -------
        a 3 value tuple of average"""
    # split image into 3 channels
    channel_r = np.average(image[:, :, 0])
    channel_g = np.average(image[:, :, 1])
    channel_b = np.average(image[:, :, 2])
    return (channel_r, channel_g, channel_b)


def __avg_grey(image):
    """ Average Intensity of the image

        return duplicate of the intensity averaged
        in 3 identical value """
    return (np.average(image))


def diff(imageA, imageB):
    """ Compare differences between imageA and imageB.
        The comparison is relative to imageA

        Parameters
        -------------
        imageA, imageB: Averaged Images

        Returns
        ---------------
        a float between 0.0 - 1.0 with 1 indicate perfect match"""
    if len(imageA) != len(imageB):
        raise DifferentBlockCountError

    if imageA is None:
        raise NullImageError

    abs_diff = 0
    num_channels = len(imageA[0])
    for A, B in zip(imageA, imageB):
        abs_diff += __diff_block(A, B) / num_channels

    result = abs_diff / len(imageA)
    if result == 0:
        return 1

    return 1 - result


def __diff_block(blockA, blockB):
    """ Determines if image is grey or color to determine
        color of grey diff function to use
    
        Parameters
        -----------
        blockA, blockB - calculated average block by blockify

        Return
        ----------
        positive float of the differences"""
    if len(blockA) == 3:
        return __diff_block_color(blockA, blockB)
    return __diff_block_grey(blockA, blockB)


def __diff_block_color(blockA, blockB):
    """ Calculate the absolute differences between two block
        of averages

        Parameters
        -----------
        blockA, blockB - calculated average block by blockify

        Return
        ----------
        positive float of the differences"""
    rA, gA, bA = blockA
    rB, gB, bB = blockB
    diff_r = abs(rA - rB) / rA
    diff_g = abs(gA - gB) / gA
    diff_b = abs(bA - bB) / bA
    return diff_r + diff_g + diff_b


def __diff_block_grey(blockA, blockB):
    """ Calculate the absolute differences between two block
            of averages

            Parameters
            -----------
            blockA, blockB - calculated average block by blockify

            Return
            ----------
            positive float of the differences"""
    return abs(blockA[0] - blockB[0]) / blockA[0]
