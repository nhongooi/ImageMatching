
import sys

__version__ = '0.1'
__banner__ = 'imageRecognition'
__usage__ = """
Image Recognition

Usage:
    {0} match [-s <type>] [-f <fuzzy>] <path> [-r <result_path>]
    {0} template [-f <fuzzy>] <template_path> <path> [-r <result_path>]
    {0} --help
    {0} --version
Options:
    -s --search=<type>     file type searched for matching
    -f --fuzzy=<fuzzy>     percentage match threshold
    -r --return=<return>   path to print result
    -h --help              show help
    -v --version           show version
 """.format(__banner__)


