
import sys
from os import path
from docopt import docopt

from . import __usage__ as usage
from . import __version__ as version
from imageRecognition import wrapper
from imageRecognition.out import formater

FILETYPE = ['archive', 'image']


def clean_args(args):
    """ run matching given by args"""
    # default values
    ret = True
    fuzzy = 100
    result_path = '.'
    filetype = None
    template_path = None
    # check if path exist as dir
    ret = isvaliddir(args['path'])

    # general args
    cleaned_path = clean_path(args['path'])
    if args['fuzzy']:
        try:
            fuzzy = int(args['fuzzy'])
        except TypeError:
            ret = False
    if args['result_path'] and isvaliddir(args['result_path']):
        result_path = clean_path(args['result_path'])

    # image processing type
    if args['match']:
        filetype = 'image'
        if args['type'] and args['type'] in FILETYPE:
            filetype = args['type']
    elif args['template']:
        if args['template'] and path.isfile(args['template']):
            template_path = clean_path(args['template'])
        else:
            ret = False

    if not ret:
        return None
    return wrapper.ImageWrapper(args['match'], result_path,
                                cleaned_path, filetype,
                                template_path, fuzzy)


def isvaliddir(path):
    if path:
        if not path.isdir(path):
            return False


def clean_path(path):
    """ Get absolute path"""
    if not path:
        return path
    fixed_path = path.expanduser(path)
    fixed_path = path.abspath(fixed_path)
    return fixed_path


def main():
    result = None
    args = docopt(usage, version)
    user_wrapper = clean_args(args)

    if user_wrapper is not None:
        result = user_wrapper.run_wrapper()

    if result is not None:
        formater.format_result(result, user_wrapper.return_path)
        print("result printed")


if __name__ == "__main__":
    main()
