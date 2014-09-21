from atxt_ import aTXT
import walking as wk
import os


def main():
    dir = "/Users/usuario/Documents/doc/"
    # dir = "/Users/usuario/Desktop/"
    i = 0
    problemas = 0
    casos = open("casos.txt", "w+")
    LEVEL = 7
    print wk.walk_size(dir, sindir=[''],
                       level=LEVEL, tfiles=[".pdf", ".docx"])
    for root, dirs, files in wk.walk(dir,
                                     level=LEVEL,
                                     tfiles=[".pdf", ".docx"]):
        for f in files:
            filepath = os.path.join(root, f.name)
            txt = aTXT(
                filepath=filepath,
                debug=True,
                uppercase=True,
                overwrite=False)
            txt.convert()
            if txt.txt_size() < (1 << 10L):
                casos.write(filepath)
                casos.write('\n')
                problemas += 1
            print i,
            i += 1

    print "#", i
    print "# dudosos", problemas
    print "revise casos.txt"

    casos.close()


if __name__ == "__main__":

    main()
