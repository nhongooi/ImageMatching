
import pytest
from imageRecognition.util import FileUtil


class TestFileutil(object):
    def test_open_img(self):
        test_path = "./testImage/[クール教信者] 小林さんちのメイドラゴン 01_pg4.jpg"
        test_none = "./testImage/doesntexistimage.jpg"
        img = FileUtil.open_img(test_path)
        img_none = FileUtil.open_img(test_none)
        assert img is not None
        assert img_none is None

    def test_iscolor(selfself):
        pass

    def test_acceptablesize(self):
        test_path = "./testImage/[クール教信者] 小林さんちのメイドラゴン 01_pg4.jpg"
        blocksize = 2
        img = FileUtil.open_img(test_path)
        img_false = [[[1]], [[1], [1]]]
        assert FileUtil.isAcceptableSize(img, blocksize)
        assert FileUtil.isAcceptableSize(img_false, blocksize) is False