
import imagehash
from PIL import Image


def hash_images(image_list, hashfunc=imagehash.average_hash):
    """ The hash algorithm will resize image into a (8,8) array which will be converted
        into greyscale resized image. Then find the mean average of the whole image. Relabel
        each pixel in 1 if the pixel is larger than average and vice versa for 0.
        When the hash object is called the object will flatten the binary array display as
        a hex hash value. This is used to compare between each image.

        Parameter
        ------------
        image_list - list of paths to image
        hashfunc - imagehash hash functions: average_hash, phash (perception hash),
        phash_simple, dhash (different hash), dhash_veritcal, whash(wavelet Hash)

        Return
        -------------
        a dictionary of hashes and image path"""
    image_hashes = {}
    hashfunc = find_hashfunc(hashfunc)
    for image in image_list:

        try:
            # create a hash object which is a binary array that
            # can generate a hash when called
            img_hash = hashfunc(Image.open(image))
            # add hash to dict
            image_hashes[img_hash] = image_hashes.get(img_hash, []) + [image]
        except Exception as e:
            print("Hashing: ", e)
    return image_hashes


def eval_hashes(image_hashes):
    """ Check hash list for duplicates

        Parameter
        ---------
        image_hashes - hashes dictionary

        Return
        ----------
        list of tuple containing matched hashes"""
    match_list = []
    # iter for each item if they have more than one hash match
    for hash, image in image_hashes.items():
        if len(image) > 1:
            match_list.append(tuple(image))
    return match_list


def find_hashfunc(hashfunc):
    if hashfunc == 'phash':
        return imagehash.phash
    elif hashfunc == 'dhash':
        return imagehash.dhash
    elif hashfunc == 'whash':
        return lambda img: imagehash.whash(img, mode='db4')
    else:
        return imagehash.average_hash