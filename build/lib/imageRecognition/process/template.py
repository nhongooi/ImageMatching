""" search through images if have a given template"""

import cv2
import numpy as np
from os import path, makedirs
from imageRecognition.util.FileUtil import open_img

CACHE = "./cache/TemplateMatches/"

def template_match(template_path, image_list, fuzzy=.8):
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
    template = cv2.imread(template_path, 0)
    check_cache_dir()
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
    return match_list

def check_cache_dir():
    if not path.isdir(CACHE):
        makedirs(CACHE)