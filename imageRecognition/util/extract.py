""" extract first image of cbz, cbr, pdf, etc and cache them to match"""
from os import path
from zipfile import ZipFile, BadZipFile
from rarfile import RarFile, BadRarFile
import re

class Extractor:

    MODE_LIST = ['single', 'all']

    def __init__(self,  cache_dir=None, mode='single'):
        """ Extract archive file type with indicated mode

            Parameters
            ----------
            mode - single - extract only first picture/page in the archive file
                   all - extract entire archive file
            cache - the folder to store extracted/thumbnailed images"""
        if mode in self.MODE_LIST:
            self.mode = mode
        # TODO find better cache path
        if cache_dir is None:
            self.cache = "./.cache/extractPath/"
        else:
            self.cache = cache_dir


    # extract will determine file type and use the correct extract function
    # this is really slow and will be converted into C at a later date
    def extract(self, file):
        """ Extract file into a cache folder if it is an archive

            Parameter
            ---------
            file = absolute path to the file

            Returns
            ---------
            list of path to the dir of theextracted file/s
            and original path as tuple"""
        filetype = self.identify_file_type(file)
        if filetype is 'cbz':
            return (file, self.__extract_cbz(file))
        elif filetype is 'cbr':
            return (file, self.__extract_cbr(file))
        elif filetype is 'pdf':
            return (file, self.__extract_pdf(file))
        else:
            raise TypeError


    def __extract_cbz(self, file):
        """ extract first image in cbz file, cache it in local cache folder"""
        try:
            archive_zip = ZipFile(file, 'r')
            extract_path =  self.cache + path.basename(file)
            if self.mode is 'all':
                archive_zip.extractall(path=extract_path)
            else:
                first_file = archive_zip.namelist()[0]
                archive_zip.extract(member=first_file, path=extract_path)
        except BadZipFile as e:
            raise e
        finally:
            archive_zip.close()
        return extract_path


    def __extract_cbr(self, file):
        """ extract first image in cbr file, cache it in local cache folder"""
        try:
            archive_rar = RarFile(file, 'r')
            extract_path = self.cache + path.basename(file)
            if self.mode is 'all':
                archive_rar.extractall(path=extract_path)
            else:
                first_file = archive_rar.namelist()[0]
                archive_rar.extract(member=first_file, path=extract_path)
        except BadRarFile as e:
            raise e
        finally:
            archive_rar.close()
        return extract_path

    # TODO not useful at this point, will be done at the end
    def __extract_pdf(self, file):
        """ extract first image in pdf file, cache it in local cache folder"""
        pass


    def identify_file_type(self, file):
        """ Determine file type of given file if it is cbz, cbr or pdf

            Parameters
            ------------
            file = absolute path to the file

             Return
             ------------
             file ext as string"""
        if re.search(u"(\.cbz)", file, re.U):
            return 'cbz'
        elif re.search(u"(\.cbr)", file, re.U):
            return 'cbr'
        elif re.search(u"(\.pdf)", file, re.U):
            return 'pdf'
        else:
            raise TypeError

