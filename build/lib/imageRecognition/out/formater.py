""" string format result"""

from os import path
FILE_HEADER = " Image Result"
FILENAME = 'result.txt'


def format_result(results, result_path):
    """ format and output result into file"""
    cleaned_path = path.join(result_path, FILENAME)
    with open(cleaned_path, 'w+') as f:
        f.write(FILE_HEADER + '\n')
        for result in results:
            str_result = "\nMatching percentage:\n{0}\n{1}\n{2}\n".format(result[0], result[1], result[2])
            f.write(str_result)

def get_resultfilename():
    return FILENAME