# -*- coding: utf-8 -*-

from aTXT import aTXT
import walking as wk
import os
import shutil as sh
import tempfile as tmp
import sys

from kitchen.text.converters import getwriter

UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)


def main():

    DIR = "/Users/usuario/Documents/bogotá"
    LEVEL = 0
    OVERWRITE = True
    UPPERCASE = False
    TFILES = ['.pdf']
    heroes = ['xpdf', 'xml']

    c_, s_ =  wk.walk_size(DIR, sdirs=[''], level=LEVEL, tfiles=TFILES)
    print c_, wk.size_str(s_)

    man = aTXT()
    for root, dirs, files in wk.walk(DIR, level=LEVEL, tfiles=TFILES):

        for f in files:
            
            man.convert(
                heroes = heroes,
                filepath=f.path,
                savein='TXT', 
                overwrite=OVERWRITE, 
                uppercase=UPPERCASE
                )
    man.close()

if __name__ == "__main__":
    main()
