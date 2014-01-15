# aTXT.py 
A extraction tool (`v0.1`) on a directory. By default traversing all inner files and folders searching files with the extension `.docx`,`.pdf`m`.doc` to convert a plain text, extension `.txt`. You can specify your requirements with `aTXT.py -help` or view below usage. 

Meta
------

- Author: Jonathan Prieto
- Email: prieto.jona@gmail.com
- Status: in development.
- Notes: Have feedback? Please send me an email. This project is still in its infancy, and will be changing rapidly.

Purpose
------

Are you needing some easy extraction tool to make your data mining analysis or whatever?. Everybody knows to handle `.txt` is so easy to read and usefull to processing.

I use this script to convert common files documents to plain text with just *doble-click*. The outcome it's just a `.txt` file for each document in the search.

Installation
-------

You can install the plugin by using pip:

```
	$ pip install aTXT
```
or, manually, by calling setup.py:
```
	$ python setup.py install
```

`aTXT.py` needs to have the next packages installed:
- `lxml` 
- `docx` 
- `pdfminer`

Usage
-----

This tool can be used in two ways:
1. Copy `aTXT.py` or execute `aTXT` in your target folder where you have the documents that you need to convert.
2. Just use the console. 
```
$ aTxt.py --pdf --docx -l
```
3. Use inside python script with `import aTXT` and the three methods described above.

In the inside of `aTXT.py` already has three main methods:  
	
- `aTXT.docx2TXT(path_file, name_file):` for the conversion of `.docx` to `.txt`
- `aTXT.pdf2TXT(path_file, name_file):` for the conversion of `.pdf` to `.txt`
- `aTXT.doc2TXT(path_file, name_file):` for the conversion of `.doc` to `.txt`

All methods above return `[ bool:Status, new_name_file]`. The `Status` is `False` if problem appear else `True`, method finished successful.


*So any idea to improve this?*  








