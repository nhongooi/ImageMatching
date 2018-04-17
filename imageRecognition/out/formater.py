""" string format result"""

from os import path
FILE_HEADER = " Image Result"
FILENAME = 'result.txt'

def format_result(results, result_path):
    """ format and output result into file"""
    if results is not None:
        cleaned_path = path.join(result_path, FILENAME)
        if len(results[0]) == 3:
            format_match(results, cleaned_path)
        else:
            format_template(results, cleaned_path)


def format_match(results, result_path):
    """ Format match result"""
    with open(result_path, 'w+') as f:
        f.write(FILE_HEADER + '\n')
        str_result = ""
        for result in results:
            str_result += "\nMatching percentage:\n{0}\n{1}\n{2}\n".format(result[0], result[1], result[2])
        f.write(str_result)

def format_template(results, result_path):
    """ Format template result"""
    with open(result_path, 'w+') as f:
        f.write(FILE_HEADER + '\n')
        str_result = ""
        for result in results:
            str_result +="\n{0}\n".format(result)
        f.write(str_result)

def get_resultfilename():
    return FILENAME