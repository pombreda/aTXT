# aTXT.py 
A extraction tool (`v0.1`).

Meta
------

- Author: Jonathan Prieto
- Email: prieto.jona@gmail.com
- Status: in development
- Notes: Have feedback? Please send me an email. his project is still in its infancy, and will be changing rapidly.

Purpose
------

Are you needing some easy extraction tool to make your data mining analysis or whatever?.

I use this script to convert common files documents to plain text. The outcome it's just a `.txt` file for each document.



In the inside of `aTXT.py` already has three main methods:  
	
- `docx2TXT(path_file, name_file):` for the conversion of `.docx` to `.txt`
- `pdf2TXT(path_file, name_file):` for the conversion of `.pdf` to `.txt`
- `doc2TXT(path_file, name_file):` for the conversion of `.doc` to `.txt`


Install
-----

You just need installed `setuptools` to call `pip`. Then, in your command line prompt (`bash`, `zsh`, `batch`) type this:

```
$	pip install aTXT
```

`aTXT.py` needs to have the next packages install:
- `lxml` 
- `docx` 
- `pdfminer`










