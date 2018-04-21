
from multiprocessing import Process, Queue
from imageRecognition.process import block, template, hashing
from imageRecognition.util import extract, crawler, FileUtil

class ImageWrapper():
    """ Wrap all image processing functionality"""

    def __init__(self, imaging_type, return_path, path, search='image',
                 template=None, fuzzy=100, hashfunc=None):
        self.type = imaging_type
        self.path = path
        self.search_filetype = search
        self.template_path = template
        self.fuzzy_percentage = fuzzy / 100
        self.return_path = return_path
        self.hashfunc = hashfunc


    def run_wrapper(self):
        """ Runs imaging processing type"""
        if self.type is 'Matching':
            if self.search_filetype == 'archive':
                self.path = FileUtil.clean_path(self.__archive_extract())

            images = self.__get_image()
            blocks = self.__blockify_image_list(images)
            return self.__eval_image(blocks)

        elif self.type is 'Templating':
            images = self.__get_image()
            match_list = template.template_match(self.template_path, images, self.fuzzy_percentage)
            return match_list

        elif self.type is 'Hashing':
            if self.search_filetype == 'archive':
                self.path = FileUtil.clean_path(self.__archive_extract())

            images = self.__get_image()
            hashes = hashing.hash_images(images, self.hashfunc)
            return hashing.eval_hashes(hashes)
        else:
            return None

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
        jobs = []
        image_split = []
        procs = 4
        image_len = len(image_list)
        # Make sure min pics run with normally
        run_procs = min(procs, image_len)
        image_split = self.__split_list(image_list, run_procs)

        # queue for process to put blocks into
        queue = Queue()
        # prepare processes
        for i in range(run_procs):
            process = Process(target=self.__blockify_per_process,
                              args=(image_split[i], queue))
            jobs.append(process)
        # start process and wait for processes to end
        for j in jobs:
            j.start()

        for j in jobs:
            blocks.extend(queue.get())

        for j in jobs:
            j.join()
        return blocks

    def __blockify_per_process(self, image_list, queue):
        """ Subprocess call blockify to add result into queue for main thread"""
        small_blocks = []
        for image in image_list:
            small_blocks.append((image, block.blockify(FileUtil.open_img(image))))

        queue.put(small_blocks)

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
        block_list_len = len(block_list)

        if block_list_len < 4:
            next_not_touch_index = 1
            for imageA in block_list:
                for index in range(next_not_touch_index,block_list_len):
                    imageB = block_list[index]
                    result = float(block.diff(imageA[1], imageB[1]))
                    if result >= self.fuzzy_percentage:
                        result = "%.2f" % result
                        compare_result.append((imageA[0],
                                               imageB[0],
                                               result))
                # to prevent images of being compare to itself and already
                # compared images in previous loops
                next_not_touch_index += 1
        else:
            jobs = []
            procs = 4
            queue = Queue()
            block_split = self.__split_list(block_list, 2)
            # prepare processes
            # The first part of the split image list will be compared to the first part and second
            # part with two processes
            # the second part work in the same way
            for i in range(procs):
                index = i % 2
                process = Process(target=self.__eval_image_process,
                                  args=(block_split[i // 2], block_split[i % 2], queue))
                jobs.append(process)
            # start process and wait for processes to end
            for j in jobs:
                j.start()

            for j in jobs:
                compare_result.extend(queue.get())

            for j in jobs:
                j.join()

        return compare_result

    def __eval_image_process(self, from_list, compare_list, queue):
        """ single process loop for evaluating image matches"""
        result_list = []
        for imageA in from_list:
            for imageB in compare_list:
                if imageA[0] is not imageB[0]:
                    result = float(block.diff(imageA[1], imageB[1]))
                    if result >= self.fuzzy_percentage:
                        result = "%.2f" % result
                        result_list.append((imageA[0],
                                               imageB[0],
                                               result))
        queue.put(result_list)

    def __split_list(self, list, procs):
        """ Reasonbly split a list into given number parts"""
        split = []
        per_tick = len(list) // procs
        for i in range(procs):
            start_tick = i * per_tick
            end_tick = start_tick + per_tick
            if i == (procs - 1):
                split.append(list[start_tick:])
            else:
                split.append(list[start_tick: end_tick])
        return split