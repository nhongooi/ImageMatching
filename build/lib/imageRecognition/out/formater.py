""" string format result"""

from os import path
FILE_HEADER = " Image Result"
FILENAME = 'result.txt'
PROCESS = ['Matching', 'Templating', 'Hashing']


def format_result(results, result_path, type):
    """ format and output result into file"""
    if results is not None:
        cleaned_path = path.join(result_path, FILENAME)
        if type is PROCESS[0]:
            format_match(results, cleaned_path)
        elif type is PROCESS[1]:
            format_template(results, cleaned_path)
        elif type is PROCESS[2]:
            format_hashing(results, cleaned_path)


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


def format_hashing(results, result_path):
    """ Format hashing result"""
    str_result = ""
    for result in results:
        str_result += "Similar Images:\n"
        for image in result:
            str_result += "{0}\n".format(image)
        str_result += "\n"

    with open(result_path, 'w+') as f:
        f.write(FILE_HEADER + "\n\n")
        f.write(str_result)


def get_resultfilename():
    return FILENAME