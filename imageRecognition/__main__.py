
import sys
from os import path
from docopt import docopt

from imageRecognition import __usage__ as usage
from imageRecognition import __version__ as version
from imageRecognition import wrapper
from imageRecognition.out import formater
from imageRecognition.util.FileUtil import clean_path

PROCESS = ['Matching', 'Templating']
FILETYPE = ['archive', 'image']


def clean_args(args):
    """ Strip user args and determine user choosen function

        Param
        -------
        args - docopt args

        Returns
        --------
        a wrapper to run user commands"""
    # default values
    ret = True
    process_type = None
    fuzzy = 100
    result_path = '.'
    filetype = None
    template_path = None
    # check if path exist as dir
    if not isvaliddir(args['<path>']):
        print("incorrect path: ", args['<path>'])
        ret = False

    # general args
    cleaned_path = clean_path(args['<path>'])
    if args['--fuzzy']:
        try:
            fuzzy = int(args['--fuzzy'])
        except TypeError:
            print("non-numerical fuzzy threshold: ", args['--fuzzy'])
            ret = False

    if args['--return'] and isvaliddir(args['--return']):
        result_path = clean_path(args['--return'])

    # image processing type
    if args['match']:
        process_type = PROCESS[0]
        filetype = FILETYPE[1]
        if args['--search'] and args['--search'] in FILETYPE:
            filetype = args['--search']
        else:
            print("Incorrect search type: ", args['--search'])
            ret = False
    elif args['template']:
        process_type = PROCESS[1]
        if args['<template_path>'] and path.isfile(args['<template_path>']):
            template_path = clean_path(args['<template_path>'])
        else:
            print("Incorrect Template path", args['<template_path>'])
            ret = False

    else:
        print("No process\n")
        ret = False

    if not ret:
        return None
    return wrapper.ImageWrapper(process_type, result_path,
                                cleaned_path, filetype,
                                template_path, fuzzy)


def isvaliddir(user_path):
    if user_path:
        if path.isdir(user_path):
            return True
        return False


def main():
    result = None
    args = docopt(usage, version=version)
    if not args:
        return False

    user_wrapper = clean_args(args)

    if user_wrapper:
        result = user_wrapper.run_wrapper()
    else:
        print("input incorrect")
        return False
    if result:
        formater.format_result(result, user_wrapper.return_path)
        print("result printed")
    else:
        print("No Matches\nPrinted Nothing")
        return False


if __name__ == "__main__":
    if main():
        sys.exit(0)
    sys.exit(1)