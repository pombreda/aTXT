#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-01-15 18:49:00
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-03-04 16:42:59


from aTXT import aTXT
import walking as wk
import sys
from kitchen.text.converters import getwriter

UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)


def main():

    # DIR = "C:\\Users\\d555\\Desktop\\doc"
    DIR = "/Users/usuario/Desktop/"
    # DIR = "C:\\Users\\A51708187\\Desktop\\bogotá"

    LEVEL = 0
    OVERWRITE = True
    UPPERCASE = False
    TFILES = ['.html']
    heroes = ['xpdf', 'xml']

    c_, s_ = wk.walk_size(DIR, sdirs=[''], level=LEVEL, tfiles=TFILES)
    print c_, wk.size_str(s_)

    man = aTXT()
    for root, dirs, files in wk.walk(DIR, level=LEVEL, tfiles=TFILES):

        for f in files:
            man.convert(
                heroes=heroes,
                filepath=f.path,
                savein='TXT',
                overwrite=OVERWRITE,
                uppercase=UPPERCASE
            )
    man.close()

if __name__ == "__main__":
    main()
