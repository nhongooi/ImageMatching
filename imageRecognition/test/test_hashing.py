
import pytest
from imageRecognition.process import hashing

class TestHashing(object):



    def test_hashing(self):
        images = ["./testImage/[クール教信者] 小林さんちのメイドラゴン 01_pg4.jpg",
                  "./testImage/[クール教信者] 小林さんちのメイドラゴン 01_pg4_eng.jpg",
                  "./testImage/TestOrig.jpg",
                  "./testImage/TestSimilar.jpg",
                  "./testImage/stock_photo.cbr",
                  "./testImage/TestOrig_copy.jpg"]
        match_pair = ("./testImage/TestOrig.jpg",
                      "./testImage/TestOrig_copy.jpg")
        hashes= hashing.hash_images(images)
        result = hashing.eval_hashes(hashes)
        for match in result:
            assert len(match) == len(match_pair)
            for single in match_pair:
                assert single in match

