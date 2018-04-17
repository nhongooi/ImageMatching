

import unittest
from imageRecognition.util.crawler import Crawler


class TestCrawler(unittest.TestCase):
    """ Test crawler"""
    def test_crawl_local(self):
        test_crawler = Crawler()
        file_list = sorted(test_crawler.crawl_local('./testImage'))
        test_list = ['TestImage.png', 'TestOrig.jpg',
                     'TestOrig_copy.jpg', 'TestSimilar.jpg',
                     '[クール教信者] 小林さんちのメイドラゴン 01_pg4.jpg',
                     '[クール教信者] 小林さんちのメイドラゴン 01_pg4_eng.jpg']

        for a, b in zip(file_list, test_list):
            self.assertTrue(b in a)
        self.assertEqual(len(file_list), len(test_list))

    def test_crawl_recur(self):
        test_crawler = Crawler()
        file_list = sorted(test_crawler.crawl_recur('./testImage'))
        test_list = ['TestImage.png', 'TestOrig.jpg',
                     'TestOrig_copy.jpg', 'TestSimilar.jpg',
                     '[クール教信者] 小林さんちのメイドラゴン 01_pg4.jpg',
                     '[クール教信者] 小林さんちのメイドラゴン 01_pg4_eng.jpg',
                     'test_jpg.jpg', 'test_png.png']

        for a, b in zip(file_list, test_list):
            self.assertTrue(b in a)
        self.assertEqual(len(file_list), len(test_list))

    def test_crawl_archive(self):
        """ Test to determine if indicated filetype was filter successfully"""
        test_crawler = Crawler(filetype='archive')
        file_list = sorted(test_crawler.crawl_recur('./testImage'))
        test_list = ['test_cbr.cbr', 'test_cbz.cbz',
                     'test_cbz.cbz', 'test_pdf.pdf']

        for a, b in zip(file_list, test_list):
            self.assertTrue(b in a)
        self.assertEqual(len(file_list), len(test_list))

    def test_crawl_ignore(self):
        """ Test successful ignore"""
        test_crawler = Crawler(ignore=u'(test_dir)')
        file_list = sorted(test_crawler.crawl_recur('./testImage'))
        test_list = ['ignore_file_image.png', 'TestImage.png', 'TestOrig.jpg',
                     'TestOrig_copy.jpg', 'TestSimilar.jpg',
                     '[クール教信者] 小林さんちのメイドラゴン 01_pg4.jpg',
                     '[クール教信者] 小林さんちのメイドラゴン 01_pg4_eng.jpg']

        for a, b in zip(file_list, test_list):
            self.assertTrue(b in a)
        self.assertEqual(len(file_list), len(test_list))
