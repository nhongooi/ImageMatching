
import unittest
import numpy as np
from imageRecognition.util.FileUtil import open_img
from imageRecognition.process.block import *


class TestImageProcessor(unittest.TestCase):
    """ Test all functions in process.block module"""

    def test_blockify_color(self):
        image = np.array([[19, 6, 3],
                            [3, 3, 3],
                            [14, 31, 6],
                            [120, 64, 12]])
        img_avg = blockify(image, block_count=1)
        test_avg = [(39,26,6)]
        self.assertEqual(img_avg, test_avg)

    def test_blockify_grey(self):
        image = np.array([[6, 6, 6],
                            [212, 212, 212],
                            [145, 145, 145],
                            [69, 69, 69]])
        img_avg = blockify(image, block_count=1)
        test_avg = [(108, 108, 108)]
        self.assertEqual(img_avg, test_avg)

    def test_compare_color_same(self):
        imgA = open_img("./testImage/TestOrig.jpg")
        imgB = open_img("./testImage/TestOrig.jpg")
        imgA_avg = blockify(imgA)
        imgB_avg = blockify(imgB)
        self.assertEqual(diff(imgA_avg, imgB_avg), 1)

    def test_compare_color_diff(self):
        imgA = open_img("./testImage/TestOrig.jpg")
        imgB = open_img("./testImage/TestImage.png")
        imgA_avg = blockify(imgA)
        imgB_avg = blockify(imgB)
        self.assertNotEqual(diff(imgA_avg, imgB_avg), 1)

    def test_compare_color_similar(self):
        imgA = open_img("./testImage/TestOrig.jpg")
        imgB = open_img("./testImage/TestSimilar.jpg")
        imgA_avg = blockify(imgA)
        imgB_avg = blockify(imgB)
        result = diff(imgA_avg, imgB_avg)
        self.assertNotEqual(result, 1)
        self.assertGreater(result, .7)

if __name__ == "__main__":
    unittest.main()