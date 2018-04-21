""" search through images if have a given template"""

import cv2
from multiprocessing import Process, Queue
from os import path, makedirs
from imageRecognition.util.FileUtil import open_img

CACHE = "./cache/TemplateMatches/"

def template_match(template, image_list, fuzzy=.8):
    """ Template match through each image, output a templated image if matched

        Parameters
        -----------
        template - template image
        image_list - list path to images to template
        threshold - percentage wanted to match with

        Returns
        ----------
        List of matched image path, result image with template written in cache folder"""
    match_list = []
    jobs = []
    image_split = []
    procs = 4
    image_len = len(image_list)
    # Make sure min pics run with normally
    run_procs = min(procs, image_len)
    per_tick = image_len // run_procs
    for i in range(run_procs):
        start_tick = i * per_tick
        end_tick = start_tick + per_tick
        if i == (run_procs - 1):
            image_split.append(image_list[start_tick:])
        else:
            image_split.append(image_list[start_tick: end_tick])


    # queue for process to put blocks into
    queue = Queue()

    check_cache_dir()
    # prepare processes
    for i in range(run_procs):
        process = Process(target=__template_split,
                          args=(template, image_split[i], queue))
        jobs.append(process)
    # start process and wait for processes to end
    for j in jobs:
        j.start()

    for j in jobs:
        match_list.extend(queue.get())

    for j in jobs:
        j.join()

    return match_list


def __template_split(template, image_list, queue):
    template = cv2.imread(template, 0)
    match_list = []
    for image in image_list:
        img_rgb = open_img(image)
        img_grey = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        width, height = template.shape[::-1]
        result = cv2.matchTemplate(img_grey, template, cv2.TM_CCOEFF_NORMED)
        # find if there is a match within the picture
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if len(max_loc) > 0:
            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            top_left = max_loc
            bottom_right = (top_left[0] + width, top_left[1] + height)
            cv2.rectangle(img_rgb, top_left, bottom_right, 255, 2)

            # write matched file with rectangle indicating templated matches
            # write to cache folder
            img_name = path.basename(image)
            cache_path = CACHE + img_name
            cv2.imwrite(cache_path, img_rgb)
            match_list.append(cache_path)

    queue.put(match_list)


def check_cache_dir():
    if not path.isdir(CACHE):
        makedirs(CACHE)