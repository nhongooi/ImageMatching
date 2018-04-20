
import sys

__version__ = '0.3'
__banner__ = 'imageRecognition'
__usage__ = """
Image Recognition

Usage:
    {0} match [-s <type>] [-f <fuzzy>] <path> [-r <result_path>]
    {0} template [-f <fuzzy>] <template_path> <path> [-r <result_path>]
    {0} hashing [-a <hashfunc>] [-s <type>] <path> [-r <result_path>]
    {0} --help
    {0} --version
Options:
    -s --search=<type>    file type searched for matching, image(default) or archive
    -f --fuzzy=<fuzzy>     percentage match threshold, 100 is default
    -r --return=<return>   path to print result, cwd is default
    -a --hashfunc=<hashfunc>   choose a type of hash algorithm in list bellow
    -h --help                show help
    -v --version           show version
Hash Functions:
    ahash - average hashing
    phash - perception hashing
    dhash - difference hashing
    whash - wavelet hashing
 """.format(__banner__)

def main():
    import imageRecognition.__main__
    if __main__.main():
        sys.exit(0)
    sys.exit(1)
