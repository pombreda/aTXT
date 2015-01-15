#!/usr/bin/env python

from version import __version__

VERSION = __version__

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup
from glob import glob

# Make data go into site-packages (http://tinyurl.com/site-pkg)
from distutils.command.install import INSTALL_SCHEMES
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']


setup(
        name = 'aTXT',
        scripts=['bin/aTXT'],
        packages = find_packages(),
        version = VERSION,
        license= 'MIT',
        description = 'A friendly Extractor of Text',
        author = 'Jonathan S. Prieto',
        author_email = 'prieto.jona@gmail.com',
        url = 'https://github.com/d555/aTXT',   # use the URL to the github repo
        download_url = 'https://github.com/d555/aTXT/' + VERSION,
        keywords = "txt doc docx pdf doc2txt docx2txt pdf2txt data conversion", # arbitrary keywords
        long_description=open('README.rst').read(),
        install_requires=[
            "lxml>=3.2.3",
            "docx>=0.2.0",
            "pdfminer",
            "docopt>=0.6.2"
        ],
        zip_safe=True,
        # entry_points = {
        #  'console_scripts': [
        #     'aTXT = bin'
        # ]
        # },
        requires=['argparse', 'docopt'],
        classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Reserchers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Operating System :: Windows',
        'Operating System :: Unix Based System',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'Topic :: Data Mining',
        'Topic :: Text Processing',
        ],       
    )
