""" string format result"""

FILE_HEADER = " Image Result"

def format_result(results):
    """ format and output result into file"""
    with open('result.txt') as f:
        f.write(FILE_HEADER, '\n' )
        for result in results:
            str_result = "\nMatching percentage: %d\n%s\n%s\n" % \
                         (result[2], result[0], result[1])
            f.write(str_result)

