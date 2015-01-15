#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-01-14 22:46:10
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-01-15 01:06:01

"""
aTXT.py
Convert files to plain text with extension (*.txt)

Usage:
    aTXT.py <file>
    aTXT.py [--from <from>] [--to <to>] <file>... 
            [-p|--pdf] [-d|--doc] [-x|--docx] [-t|--dat]
    aTXT.py --path <path> [--depth <depth>] [--to <to>] 
            [-p|--pdf] [-d|--doc] [-x|--docx] [-t|--dat]
    aTXT.py [-h|--help]

Arguments:
    <file>            If <from> is none, file should be in current directory
    --path  <path>    Process the folder with path <path> and all files inside

Options:
    --from <from>     Process files from path <from> if <file> appears
    --to <to>         Save all (*.txt) files to path <to> if <file> appears
    --depth <depth>   Depth for trasvering path using depth-first-search 
                      for --path option
    -p, --pdf         Convert files with extension *.pdf or *.PDF
    -x, --docx        Convert files with extension *.docx or *.DOCX
    -d, --doc         Convert files with extension *.doc or *.DOC
    -t, --dat         Convert files with extension *.dat or *.DAT
    -h, --help        Print this help
    -v, --version     Print current version installed
"""

from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__, version='aTXT ')
    if args['<file>']:
        print "entro a file"
    elif args['<path>']:
        print "entro a path"
    else:
        print __doc__

