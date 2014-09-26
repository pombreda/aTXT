# -*- coding: utf-8 -*-

from aTXT import aTXT
import walking as wk
import os
import shutil as sh
import tempfile as tmp
import sys

from kitchen.text.converters import to_unicode,getwriter

UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

# encoding = locale.getpreferredencoding()
# Writer = getwriter(encoding)
# sys.stdout = Writer(sys.stdout)

def main():


    dir = to_unicode("D:\\textos bogotá", 'utf-8')
    casos_dir = os.path.join(dir, "raros")
    txt_dirs = os.path.join(dir, "txt_dirs")
    all_dirs = os.path.join(dir, "all_dirs")
    LEVEL = 0
    OVERWRITE = True
    # TFILES = ['.pdf', '.doc', '.docx']
    TFILES = ['.pdf']

    try:
        os.makedirs(casos_dir)
    except Exception, e:
        pass
    try:
        os.makedirs(txt_dirs)
    except Exception, e:
        pass

    try:
        os.makedirs(all_dirs)
    except Exception, e:
        pass

    i = 0
    problemas = 0
    c_, s_ = wk.walk_size(dir, sdirs=[''],
                          level=LEVEL, tfiles=TFILES)
    print c_, wk.size_str(s_)

    tpath = tmp.mkdtemp()

    for root, dirs, files in wk.walk(dir,
                                     level=LEVEL,
                                     tfiles=TFILES):
    	# root = to_unicode(root, 'utf-8')

        for f in files:
            filepath = os.path.join(root, f.name)
            txt = aTXT(
                filepath=filepath,
                debug=True,
                uppercase=False,
                overwrite=OVERWRITE)

            txt.convert()
            print txt.txt_path
            print i,
            try:
                print filepath,
            except:
                print "name",

            if txt.txt_size() < (1 << 10L):
                problemas += 1
                try:
                    sh.copy2(filepath, casos_dir)
                except Exception, e:
                    try:
                        print e
                        print "fail to copy", filepath, "to", casos_dir
                    except:
                        pass

                try:
                    sh.copy2(txt.txt_path, txt_dirs)
                except Exception, e:
                    try:
                        print e
                        print "fail to copy", txt.txt_path, "to", txt_dirs
                    except:
                        pass
            else:
                try:
                    sh.copy2(txt.txt_path, all_dirs)
                except Exception, e:
                    pass
            print txt.txt_size()
            print txt.txt_path
            print "Finish"

            i += 1

    print "#", i
    print "# dudosos", problemas
    try:
        sh.rmtree(tpath)
    except:
        pass


if __name__ == "__main__":

    main()
