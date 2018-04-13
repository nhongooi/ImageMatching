#! /usr/bin/env python

from setuptools import setup, find_packages

readme = open('README').read()

VERSION = '0.1'
REQUIRES_PYTHON = "==3.6"

setup(
    name='imageRegcognition',
    version=VERSION,
    description="match duplicate images",
    long_description= readme,
    author='Tim Nguyen',
    author_email="tug56656@temple.edu",
    install_requires=['numpy',
                      'opencv-python >=3.4.0.12',
                      'rarfile', 'docopt'],
    python_requires=REQUIRES_PYTHON,
    classifiers=[
            "Programming Language :: Python :: 3.6",
            "Operating System :: POSIX :: Linux",
          ],
    packages=find_packages(exclude=['tests*']),
    extras_require= {
        'test': ['pytest']
    },
    
    entry_points={
        'console_scripts': [
            'imageRecognition=main:main',
        ],
    },
)