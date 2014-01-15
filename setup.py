#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from glob import glob

# Make data go into site-packages (http://tinyurl.com/site-pkg)
from distutils.command.install import INSTALL_SCHEMES
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']



setup(
        name = 'aTXT',
        packages = ['aTXT'], # this must be the same as the name above
        py_modules=['aTXT'],
        version = '0.1',
        description = 'An easy conversion of docx, pdf, doc(windows) to txt format file. Extraction`s tool.',
        author = 'Jonathan Prieto',
        author_email = 'prieto.jona@gmail.com',
        url = 'https://github.com/d555/aTXT',   # use the URL to the github repo
        download_url = 'https://github.com/d555/aTXT/0.1',
        keywords = ['doc', 'docx', 'pdf', 'docx2txt', 'pdf2txt', 'doc2txt', 'txt', 'extraction', 'office'], # arbitrary keywords
        classifiers = [],
        install_requires=[
            "lxml>=3.2.3",
            "docx>=0.2.0",
            "pdfminer"
        ],
    )
