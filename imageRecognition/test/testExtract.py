
import unittest
from os import remove
from os.path import isdir, isfile
import shutil
from imageRecognition.util.extract import Extractor

class TestExtract(unittest.TestCase):

    def test_idenitify_fuletype(self):
        extractor = Extractor()
        test_cbr = "test_cbr.cbr"
        test_cbz = "test_cbr.cbz"
        test_zip = "test_cbr.zip"
        self.assertEqual(extractor.identify_file_type(test_cbr), 'cbr')
        self.assertEqual(extractor.identify_file_type(test_cbz), 'cbz')
        with self.assertRaises(TypeError):
            extractor.identify_file_type(test_zip)

    def test_extract_cbr(self):
        extractor = Extractor()
        test_cbz = "./testImage/[クール教信者] 小林さんちのメイドラゴン 01_pg4.jpg.cbz"
        test_cbz_extract = extractor.extract(test_cbz)
        self.assertTrue(isdir(test_cbz_extract[1]))
        # remove file after extracted
        shutil.rmtree(test_cbz_extract[1])

    def test_extract_cbz(self):
        extractor = Extractor()
        test_cbr = "./testImage/stock_photo.cbr"
        test_cbr_extract = extractor.extract(test_cbr)
        self.assertTrue(isdir(test_cbr_extract[1]))
        # remove file after extracted
        shutil.rmtree(test_cbr_extract[1])

    def test_extract_pdf(self):
        extractor = Extractor()
        test_pdf = "./testImage/[クール教信者] 小林さんちのメイドラゴン 01_pg4.pdf"
        test_pdf_extract = extractor.extract(test_pdf)
        self.assertTrue(isfile(test_pdf_extract[1]))
        # remove file after extracted
        remove(test_pdf_extract)
