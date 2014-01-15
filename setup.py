#!/usr/bin/env python

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
        packages = find_packages(),
        py_modules=['aTXT'],
        version = '0.1.1',
        license= 'MIT',
        platform ='*nix, windows with office/win32comlib',
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
        zip_safe=True,
        scripts=['aTXT.py'],
        entry_points = {
         'console_scripts': [
            'aTXT = aTXT:main'
        ]
        },
    )
