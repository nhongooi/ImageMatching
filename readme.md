# Image Recognition

A python command-line interface program to find duplicate image.

It has a function to match through a directory and find all matches above a given 
threshold. Every functions will use parallelism to run 4 or less processes for computation and comparing result, excluding the main process. 

## Requirements

The program requires these packages:
* numpy
* opencv-python
* rarfile
* docopt
* pillow
* imagehash
* pdf2image
* Pypdf2       

## Build

Run:

        python3 setup.py install

The python setuptool will setup the python program and its depedencies.

## The type of matches:

### Match		  

Match image to image, regarless of size, and marked as a match if pass a the given 
threshold, fuzzy, in a given PATH. If given type to search for, which can be  
archive or image, the program will recursively search through a given directory and  
match each found image to another image. If given an archive, images will be extracted to a 
cache directory for matching. A result will be output with given image paths and match percentage.

### Template

Find if a template_path is in a list of image in given <path> and will save the 
matches with a blue box if the template reach the given threshold, fuzzy.   
 
### Hashing 
 
 This match image by convert the image into a greyscale 8 by 8 with antialias filtering,  perform a hashing
 algorithm listed within the hash functions below. If the hash value are the same, the images are consider
 the same image. There has been variation of similar images accounted, This algorithm is more strict than
 simple matching, but still allows some variability. An example would be a picture with an a person eating
 comparing to closing their mouth.

## Command-Line Help

Usage:

    imageRecognition match [-s <type>] [-f <fuzzy>] <path> [-r <result_path>]
    imageRecognition template [-f <fuzzy>] <template_path> <path> [-r <result_path>]
    imageRecognition hashing [-a <hashfunc>] [-s <type>] <path> [-r <result_path>]
    imageRecognition --help
    imageRecognition --version
    
Options:

    -s --search=<type>                file type searched for matching, image(default) or archive
    -f --fuzzy=<fuzzy>                percentage match threshold, 100 is default
    -r --return=<return>              path to print result, cwd is default
    -a --hashfunc=<hashfunc>          choose a type of hash algorithm in list bellow
    -h --help                         show help
    -v --version                      how version
    
Hash Functions:

    ahash - average hashing
    phash - perception hashing
    dhash - difference hashing
    whash - wavelet hashing

## Known Bugs

* The pathing for every function is for linux filesystem. So this might not work on windows.
* Match function tends to do terrible when there is lack of diversity in color of the image. Ex: A majority white image will likely to give higher probability.
* Template function can give wrong location of the template in some high pixel density images, when using low pixel density template
* Template depending on resolution, it might takes up more memory than usual, but sufficient for a 32bit system and is not a concern on 64 bit.
