""" search through images if have a given template"""

import cv2
import numpy as np
from os import path
from imageRecognition.util.FileUtil import open_img

CACHE = "./.cache/TemplateMatches/"

def template_match(template, image_list, threshold=80):
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
    for image in image_list:
        img_rgb = open_img(image)
        img_grey = cv2.cvtColor(img_rgb, cv2.COLOR_BayerRG2GRAY)
        img_template = open_img(template)

        width, height = img_template.shape[::-1]
        result = cv2.matchTemplate(img_grey, img_template, cv2.CV_TM_CCORR)
        found_loc = np.where(result <= threshold)
        if len(found_loc) >= 0:
            for point in zip(*found_loc[::-1]):
                cv2.rectangle(img_rgb, point,
                              (point[0] + width, point[1] + height),
                              (0, 255, 255), 2)
            # write matched file with rectnagle indicating templated matches
            # write to cache folder
            img_name = path.basename(image)
            cache_path = CACHE + img_name
            cv2.imwrite(cache_path, img_rgb)

            match_list .append(image)
    return match_list