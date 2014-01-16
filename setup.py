#!/usr/bin/env python
'''
aTXT.py
=======

A extraction tool (``v0.1``) on a directory. By default traversing all
inner files and folders searching files with the extension
``.docx``,\ ``.pdf``\ m\ ``.doc`` to convert a plain text, extension
``.txt``. You can specify your requirements with ``aTXT.py -help`` or
view below usage.

Meta
----

-  Author: Jonathan Prieto
-  Email: prieto.jona@gmail.com
-  Status: in development.
-  Notes: Have feedback? Please send me an email. This project is still
   in its infancy, and will be changing rapidly.

Purpose
-------

Are you needing some easy extraction tool to make your data mining
analysis or whatever?. Everybody knows to handle ``.txt`` is so easy to
read and usefull to processing.

I use this script to convert common files documents to plain text with
just *doble-click*. The outcome it's just a ``.txt`` file for each
document in the search.

Installation
------------

You can install the plugin by using pip:

::

        $ pip install aTXT

or, manually, by calling setup.py:

::

        $ python setup.py install

``aTXT.py`` needs to have the next packages installed: - ``lxml`` -
``docx`` - ``pdfminer``

If you run on **Windows** and you want to convert ``.doc`` files. You
need to install: ``win32com``. You can get it
``http://sourceforge.net/projects/pywin32/files/pywin32/Build%20218/``.

Usage
-----

This tool can be used in two ways: 1. Copy ``aTXT.py`` or execute
``aTXT`` in your target folder where you have the documents that you
need to convert. 2. Just use the console.

::

    $ aTXT.py --pdf --docx -l

3. Use inside python script with ``import aTXT`` and the three methods
   described above.

In the inside of ``aTXT.py`` already has three main methods:

-  ``aTXT.docx2TXT(path_file, name_file):`` for the conversion of
   ``.docx`` to ``.txt``
-  ``aTXT.pdf2TXT(path_file, name_file):`` for the conversion of
   ``.pdf`` to ``.txt``
-  ``aTXT.doc2TXT(path_file, name_file):`` for the conversion of
   ``.doc`` to ``.txt``

All methods above return ``[ bool:Status, new_name_file]``. The
``Status`` is ``False`` if problem appears else ``True``, method
finished successful.

*So any idea to improve this?*
'''

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup
from glob import glob

# Make data go into site-packages (http://tinyurl.com/site-pkg)
from distutils.command.install import INSTALL_SCHEMES
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

def find_version():
    return "0.1.3"

setup(
        name = 'aTXT',
        packages = find_packages(),
        py_modules=['aTXT'],
        version = find_version(),
        license= 'MIT',
        description = 'An easy conversion of docx, pdf, doc(windows) to txt format file. Extraction`s tool.',
        author = 'Jonathan Prieto',
        author_email = 'prieto.jona@gmail.com',
        url = 'https://github.com/d555/aTXT',   # use the URL to the github repo
        download_url = 'https://github.com/d555/aTXT/' + find_version(),
        keywords = "extract txt doc docx pdf doc2txt docx2txt pdf2txt", # arbitrary keywords
        classifiers = [],
        long_description=open('README.rst').read(),
        install_requires=[
            "cli_tools",
            "lxml>=3.2.3",
            "docx>=0.2.0",
            "pdfminer"
        ],
        zip_safe=True,
        scripts=['aTXT.py'],
        entry_points = {
         'console_scripts': [
            'aTXT = aTXT:main.console'
        ]
        },
       
    )
