""" traverse through directory/ies and record each img path"""
import re
from os import listdir, walk
from os.path import isfile, isdir, join

class Crawler:
    HIDDEN = u"(\/\..*)"
    IMAGE_FORMAT = u"(\.jpeg|\.jpg|\.bmp|\.png)"
    ARCHIVE_FORMAT = u"(\.cbr|\.cbz|\.pdf)"

    # https://stackoverflow.com/questions/43580/how-to-find-the-mime-type-of-a-file-in-python
    # alternative use to identify file type, but it needs another python lib
    def __init__(self, ignore='hidden', filetype='image'):
        """ Init a file crawler that can recusively itterate through a
            directory and list all file

            Parameters
            -----------
            ignore - use python regex to ignore searches
                     default is linux hidden folders and its file
            fileType - either image or archive filetype
                image - jpeg, bmp, png
                archive - cbz, cbr, pdf, epub"""
        if ignore is 'hidden':
            # ignore hidden dir in linux
            self.ignore = self.HIDDEN
        else:
            self.ignore = ignore

        if filetype is 'image':
            self.fileType = self.IMAGE_FORMAT
        else:
            self.fileType = self.ARCHIVE_FORMAT

    def crawl_local(self, path):
        """ Crawl through path to find all instances of a file
            in path

            Parameters
            ----------
            path - absolute path to directory

            Returns
            ------------
            list of all files in path, locally"""
        image_search = re.compile(self.fileType, re.U)
        return [f for f in listdir(path) if isfile(join(path, f))
                                         and image_search.search(f)]

    #https://stackoverflow.com/questions/120656/directory-listing-in-python
    def crawl_recur(self, path):
        """ Tree crawl through path to find all instances of a file recursively.
            Filter dir wanted to be ignored
            filter file that is not desired file type

            Parameters
            ----------
            path - absolute path to directory

            Returns
            ------------
            list of all files in path"""
        file_list = []
        if not isdir(path):
            raise NotADirectoryError
        # use regex to remove ignore and files not wanting
        ignore_search = re.compile(self.ignore, re.U)
        image_search = re.compile(self.fileType, re.U)
        for dirname, subdirs, files in walk(path):
            if ignore_search.search(dirname):
                continue
            for file in files:
                if image_search.search(file):
                    file_list.append(join(dirname, file))
        return file_list
