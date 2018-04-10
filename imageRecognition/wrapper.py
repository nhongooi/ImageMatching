
from imageRecognition.process import block, template
from imageRecognition.util import extract, crawler, FileUtil
from imageRecognition.out import formater

class ImageWrapper():
    """ Wrap all image processing functionality"""

    def __init__(self, imaging_type, path, search=None,
                 template=None, fuzzy=100):
        self.type = imaging_type
        self.path = path
        self.search_filetype = search
        self.template_path = template
        self.fuzzy_percentage = fuzzy

    def run_wrapper(self):
        """ Runs imaging processing type"""
        if self.type is 'Matching':
            if self.search_filetype is 'Archive':
                self.path = self.__archive_extract()

            images = self.__get_image()
            blocks = self.__blockify_image_list(images)
            return self.__eval_image(blocks)

        # UI only gave two option, so it cant be anything else
        else:
            self.__template_wrapper()

    def __archive_extract(self):
        """ Create the necessary environment to extract and return the path
            where the image extracted are being cached

            Returns
            --------
            cache directory of extracted archive/s"""
        # init crawler with archive file type
        arc_crawler = crawler.Crawler(filetype=self.search_filetype)
        # find all files in path, that is an acceptable archive type
        archive_list = arc_crawler.crawl_recur(self.path)
        # init extract that only extract first file of archive
        single_img_extractor = extract.Extractor()
        # extract every files that is an archive into cache folder
        for file in archive_list:
            single_img_extractor.extract(file)
        cache_path = single_img_extractor.cache

        return cache_path


    def __get_image(self):
        """ Go through a directory to collect all images

            Return
            -------
            list of path to images"""
        img_crawler = crawler.Crawler()
        return img_crawler.crawl_recur(self.path)

    def __blockify_image_list(self, image_list):
        """ blockify and average every image in image_list

            Return
            ------
            a list of Tuple of image path and its averaged blocks"""
        blocks = []

        for image in image_list:
            with FileUtil.open_img(image) as i:
                blocks.append((image, block.blockify(image=i)))

        return blocks

    def __eval_image(self, block_list):
        """ evaluate differences between each image to another
            If evaluation result is higher or equal to desired
            percentage, it is a match

            Parameter
            ---------
            block_list -  list of Tuple of image path and
                          its averaged blocks

            Returns
            ---------
            A list of tuples of matching image with its maching image
            in a form of (imageA, imageB, result in int)"""

        compare_result = []

        next_not_touch_index = 1
        block_list_len = len(block_list)

        for imageA in block_list:
            for index in range(next_not_touch_index,block_list_len):
                imageB = block_list[index]
                result = int(block.diff(imageA[1], imageB[1]))
                if result >= self.fuzzy_percentage:
                    compare_result.append((imageA[0],
                                           imageB[0],
                                           result))
            # to prevent images of being compare to itself and already
            # compared images in previous loops
            next_not_touch_index += 1

        return compare_result

    def __template_wrapper(self):
        pass
