#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division

__author__ = 'Jonathan Prieto'
__version__ = "0.2"

import os
import tempfile as tmp
import walking as wk

import docx.docx as docx
from pdfminer import layout, pdfinterp, converter, pdfpage
from latin2ascii import *
import sys
import subprocess as sub
import shutil as sh
import logging as log
import zipfile as zp
import datetime

from kitchen.text.converters import getwriter, to_unicode

UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

# log_filename = "aTXT" + \
#     datetime.datetime.now().strftime("-%Y_%m_%d_%H-%M") + ".log"
log_filename = "LOG.txt"


class Debug(object):

    def __init__(self, log_path=log_filename, debug=True):
        self.debug = debug
        log.basicConfig(filename=log_path,
                        filemode='w',
                        level=log.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%y %I:%M:%S %p | '
                        )

    def write(self, msg, *args):
        if not self.debug:
            pass
        try:
            if type(msg) is type(lambda x: x):
                log.debug(msg.func_name)
                for arg in args:
                    log.debug("\t{0}".format(args))
            else:
                log.debug(msg + ' ' + ' '.join(args))
        except:
            log.debug(msg)
            for arg in args:
                log.debug(arg)


class File(object):
    _debug = Debug()

    def __init__(self, path, debug=None):
        self.debug('FileClass')
        if not debug:
            self._debug = debug
        try:
            self.path = to_unicode(path)
        except Exception, e:
            self.path = path
            self.debug(e)

        try:
            self.basename = os.path.basename(self.path)
            self.name, self.extension = os.path.splitext(self.basename)
            self.extension = self.extension.lower()
            self.dirname = os.path.dirname(self.path)
        except Exception, e:
            self.debug(e)
        self.to_str()

    def debug(self, *args):
        self._debug.write(*args)

    def remove(self):
        if os.path.isfile(self.path):
            try:
                sh.remove(self.path)
                self.debug("File deleted", self.path)
                return 1
            except:
                self.debug("*", "Failed remove file", self.path)
        return 0

    def size(self):
        if not os.path.isfile(self.path):
            self.debug("is not a file", self.path)
            return 0
        size = os.path.getsize(self.path)
        self.debug("Size:", wk.size_str(size))
        return size

    def move(self, topath=None):
        if not topath:
            return False
        try:
            self.debug("moving from", self.path, "to", topath)
            sh.copy2(self.path, topath)
            self.debug("file moved")
        except Exception, e:
            self.debug("*", "fail moving file", e)
        return topath

    def to_str(self):
        self.debug("\t", self.basename)
        print self.basename

        self.debug("\t", self.path)
        print self.path

        print self.size()

        test = os.path.isdir(self.dirname), os.path.isfile(self.path)
        self.debug("\t", "test: (exist dirname, exist filepath)", test)
        print "\t", "test:", test

        print "==============="

    def create_temp(self, tempdir=None):
        if not tempdir or not os.path.exists(tempdir):
            try:
                self.debug("creating a temporary directory")
                self._tempdir = tmp.mkdtemp()
                self.debug(self._tempdir)
            except Exception, e:
                self.debug("* fail to create directory", e)
        else:
            self._tempdir = tempdir
        try:
            self.debug(
                "from temp()", "copy ", self.basename, "to ", self._tempdir)
            sh.copy2(self.path, self._tempdir)
        except:
            self.debug("* fail to copy of", self.basename, "to", self._tempdir)

        self._name = "temp"
        self._basename = self._name + self.extension
        self._path = os.path.join(self._tempdir, self._basename)
        try:
            self.debug("change name for security: " + self._basename)
            os.rename(os.path.join(self._tempdir, self.basename), self._path)
        except Exception, e:
            self.debug("fail to change name to 1.pdf", e)


class aTXT(object):
    overwrite = True
    uppercase = False
    savein = 'TXT'
    hero_docx = 'python-docx'
    hero_pdf = 'xpdf'

    def __init__(self, debug=False, lang='spa', msword=None, use_temp=False):
        self._debug = debug
        if not debug:
            self._debug = Debug()

        self.debug("aTXT Version: " + __version__ + ":" * 50)

        # basic setting
        self.lang = lang
        self.use_temp = use_temp
        if not msword:
            try:
                from win32com import client
                self.msword = client.DispatchEx("Word.Application")
                self.msword.Visible = False
            except:
                self.debug("It's not available win32com")

        # TESSERACT AND OTHERS BINARIES
        self.tesseract_required = "3.02.02"
        self.xpdf_required = "3.04"

        if sys.platform in ["win32"]:
            self.debug('set thirdy paths for win32')
            try:
                self.xpdf_path = os.path.join(os.curdir, 'bin', 'win', 'bin64')
                self.pdftotext = os.path.join(self.xpdf_path, 'pdftotext.exe')
                self.pdftopng = os.path.join(self.xpdf_path, 'pdftopng.exe')
                self.pdffonts = os.path.join(self.xpdf_path, 'pdffonts.exe')
            except:
                self.debug('fail set thirdy paths for win32')

        elif sys.platform in ["darwin"]:
            self.debug('set thirdy paths for darwin mac')
            try:
                self.xpdf_path = os.path.join(os.curdir, 'bin', 'mac', 'bin64')
                self.pdftotext = os.path.join(self.xpdf_path, 'pdftotext')
                self.pdftopng = os.path.join(self.xpdf_path, 'pdftopng')
                self.pdffonts = os.path.join(self.xpdf_path, 'pdffonts')
            except:
                self.debug('fail set thirdy paths for darwin mac')

        if not os.path.exists(self.pdftotext):
            self.debug("not exists", self.pdftotext)
        if not os.path.exists(self.pdftopng):
            self.debug("not exists", self.pdftopng)

        self.debug('set path for tesseract OCR')

        if str(os.name) == 'nt':
            self.tesseract_binary = '"c:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"'
        else:
            self.tesseract_binary = "/usr/local/bin/tesseract"
            if self.debug:
                try:
                    self.debug(
                        "trying to find tesseract binary by which command")
                    self.tesseract_binary = sub.check_output(
                        ['which', 'tesseract']).rstrip()
                except:
                    self.debug("*", "fail with which commnand")
                self.debug("set tesseract: ", self.tesseract_binary)
        self.debug("Ready to start any conversion")
        self.debug("")

    def close(self):
        self.debug('Close aTXT '+':'*50)
        try:
            self.msword.Quit()
        except:
            pass
        self.debug('Finish work')

    def debug(self, *args):
        self._debug.write(*args)

    def make_dir(self, path):
        try:
            os.makedirs(path)
            self.debug('\tDirectory created:', path)
        except Exception, e:
            self.debug("\t", e)

        if not os.access(path, os.W_OK):
            self.debug('\tDirectory without permissions: %s' % path)
            return 0
        return 1

    def remove_dir(self, path):
        if os.path.isdir(path):
            try:
                sh.rmtree(path)
                self.debug("Directory removed", path)
                return 1
            except:
                self.debug("*", "Failed remove directory", path)
        return 0

    def set(self, filepath, savein='TXT', overwrite='True', uppercase='False'):
        self.debug("Set configuration for file:")
        try:
            self.file = File(filepath, debug=self._debug)
            self.debug("\tsuccessful instance of file")
        except Exception, e:
            self.debug("\tfail creating File object")
            self.debug(e)

        self.debug("\t", self.file.basename)

        try:
            self.debug('\ttrying to encode utf-8 savein')
            self.savein = to_unicode(self.savein, 'utf-8')
        except:
            self.debug('\tfail to encode utf-8')

        if not os.path.isdir(savein):
            self.savein = os.path.join(self.file.dirname, savein)
            self.make_dir(self.savein)
    
        self.debug('\tfile will be save in', self.savein)

        if type(overwrite) == type(True):
            self.overwrite = overwrite

        if type(uppercase) == type(True):
            self.uppercase = uppercase

        self.txt = None
        try:
            path=os.path.join(self.savein,  self.file.name + ".txt")
            self.debug("\tsetting .txt file", path)
            self.txt = File(path,self._debug)
        except Exception, e:
            self.debug("\tfail to create txt file", e)

    def from_docx(self, hero='xml', filepath='', savein='', overwrite='', uppercase=''):
        try:
            self.set(filepath, savein, overwrite, uppercase)
        except Exception, e:
            self.debug(e)

        self.debug('_'*50)
        self.debug('[new conversion]')
        self.debug('\tfrom_docx starting')

        if not self.overwrite and os.path.exists(self.txt.path):
            return self.txt.path

        try:
            self.debug("\tfrom_docx", "creating file", self.txt.path)
            self.txt.doc = open(self.txt.path, "w")
            self.debug("\tfrom_docx", "file created", self.txt.path)
        except Exception, e:
            self.debug("\t*from_docx fail to create", self.txt.path)
            self.debug(e)
            return ''

        self.debug('\tfrom_docx', 'hero =', hero)
        if hero == "python-docx":
            self.debug('\tfrom_docx using python-docx')
            doc_ = docx.opendocx(self.file.path)
            for line in docx.getdocumenttext(doc_):
                try:
                    line = latin2ascii(unicode(line, 'utf-8', 'ignore'))
                except:
                    pass
                try:
                    line = line.encode('utf-8', 'replace')
                except:
                    pass
                self.txt.doc.write(line + '\n')
            self.txt.doc.close()
            self.debug("\tfinish work with .docx")
            return self.txt.path
        try:
            self.txt.doc.write(self.from_docx_())
        except Exception, e:
            self.debug("\t* from_docx_ error", e)
            return ''
        return self.txt.path

    def from_docx_(self):
        '''
         http://stackoverflow.com/questions/42482/best-way-to-extract-text-from-a-word-doc-
         without-using-com-automation
        '''
        try:
            from xml.etree.cElementTree import XML
        except:
            self.debug("*", "from_docx_ failed XML")
            from xml.etree.ElementTree import XML

        WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
        PARA = WORD_NAMESPACE + 'p'
        TEXT = WORD_NAMESPACE + 't'

        document = zp.ZipFile(self.file.path)

        self.debug("\tfrom_docx_ zipfile open document")
        xml_content = document.read('word/document.xml')

        self.debug("\ttfrom_docx_ close document")
        document.close()

        self.debug("\tfrom_docx_ XML(xml_content)")
        tree = XML(xml_content)
        paragraphs = []

        self.debug("\tfrom_docx_ tree.iterator")
        for paragraph in tree.getiterator(PARA):
            line = [
                node.text for node in paragraph.getiterator(TEXT) if node.text]
            line = ''.join(line)
            try:
                line = latin2ascii(unicode(line, 'utf-8', 'ignore'))
            except:
                pass
            try:
                line = line.encode('utf-8', 'replace')
            except:
                pass
            if line:
                paragraphs.append(line)
        return '\n\n'.join(paragraphs)

    def from_doc(self, filepath='', savein='', overwrite='', uppercase=''):
        try:
            self.set(filepath, savein, overwrite, uppercase)
        except Exception, e:
            self.debug(e)

        self.debug('_'*50)
        self.debug('[new conversion]')
        self.debug('\tfrom_doc starting')

        if not self.overwrite and os.path.exists(self.txt.path):
            return self.txt.path

        cerrar = False

        if not self.msword:
            try:
                self.msword = client.DispatchEx("Word.Application") # Using DispatchEx for an entirely new Word instance
                self.msword.Visible = False
                cerrar = True
            except Exception, e:
                self.debug("fail Dispatching Word.Application")
                return ''

            try:
                self.debug("from_doc", "opening file", self._path)
                # http://msdn.microsoft.com/en-us/library/bb216319%28office.12%29.aspx
                # wb = self.msword.Documents.Open(
                wb = self.msword.Documents.OpenNoRepairDialog(
                    FileName = self._path,
                    ConfirmConversions = False,
                    ReadOnly = True,
                    AddToRecentFiles = False,
                    # PasswordDocument,
                    # PasswordTemplate,
                    Revert = True,
                    # WritePasswordDocument,
                    # WritePasswordTemplate,
                    # Format,
                    # Encoding,
                    Visible = False,
                    # OpenConflictDocument,
                    OpenAndRepair = True,
                    # DocumentDirection,
                    NoEncodingDialog = True
                    )

            except Exception, e:
                self.debug("from_doc", "fail open file with Word", e)
                self.remove_file(self.txt.path)
                return ''

            try:
                self.debug("from_doc", "saving file", self.txt.path)
                wb.SaveAs(self.txt.path, FileFormat=2)
            except Exception, e:
                self.debug("from_doc", "fail to save file", e)
                self.remove_file(self.txt.path)
                return ''

            self.debug("from_doc", "closing file")
            wb.Close()
            self.debug("from_doc", "closing word office")
            if cerrar:
                self.msword.Quit()
            return self.txt.path
        return ''

    def from_pdf(self, hero='xpdf', filepath='', savein='', overwrite='', uppercase=''):
        try:
            self.set(filepath, savein, overwrite, uppercase)
        except Exception, e:
            self.debug(e)
        self.debug('_'*50)
        self.debug('[new conversion]')
        self.debug('starting pdf to txt')

        if not self.overwrite and os.path.exists(self.txt.path):
            self.debug(self.txt.path, "yet exists")
            return self.txt.path

        try:
            self.debug("from_pdf opening to read", self.file.path)
            doc_ = file(self.file.path, 'rb')
        except Exception, e:
            self.debug("* from_pdf", e)
            return ''
        try:
            self.debug("from_pdf creating to write", self.txt.path)
            f = file(self.txt.path, "wb")
            self.debug("from_pdf created", self.txt.basename)
        except Exception, e:
            self.debug("* from_pdf", e)
            return ''

        self.debug("\thero:" + hero)

        if hero == "pdfminer":
            try:
                self.debug("from_pdf", "creating PDFResourceManager")
                resourceman = pdfinterp.PDFResourceManager()
                self.debug("from_pdf",  "using TextConverter")
                device = converter.TextConverter(
                    resourceman, f, laparams=layout.LAParams())
                self.debug("from_pdf",  "using PDFPageInterpreter")
                interpreter = pdfinterp.PDFPageInterpreter(resourceman, device)
                for page in pdfpage.PDFPage.get_pages(doc_):
                    interpreter.process_page(page)
                f.close()
                device.close()
            except Exception, e:
                self.debug("* from_pdf", e)
                return ''

        if hero == "xpdf":
            try:
                self.debug("from_pdf", "xpdf")
                try:
                    options = [self.pdftotext, unicode(self.file.path), '-']
                except:
                    options = [self.pdftotext, self.file.path, '-']

                self.debug("from_pdf", options)
                self.debug("from_pdf", "starting subprocess")
                output = sub.call(options, stdout=f)
                self.debug("from_pdf", "finished subprocess")
                if output == 0:
                    self.debug("from_pdf", "No error.")
                elif output == 1:
                    self.debug("from_pdf", "Error opening a PDF file.")
                elif output == 2:
                    self.debug("from_pdf", "Error opening an output file.")
                elif output == 3:
                    self.debug(
                        "from_pdf", "Error related to PDF permissions.")
                else:
                    self.debug("from_pdf", "Other error.")
            except Exception, e:
                self.debug("*", "from_pdf", e)
        f.close()
        doc_.close()
        return self.txt.path
    
    def from_pdf_ocr(self, hero="xpdf", filepath='', savein='', overwrite='', uppercase='',force=False):
        try:
            self.set(filepath, savein, overwrite, uppercase)
        except Exception, e:
            self.debug(e)
        self.debug('_'*50)
        self.debug('[new conversion]')
        self.debug('starting pdf_ocr to txt')

        if not self.overwrite and os.path.exists(self.txt.path):
            self.debug(self.txt.path, "yet exists")
            return self.txt.path

        self.debug("from_pdf_ocr", "creating temporary file of file")
        try:
            self.file.create_temp()
        except Exception, e:
            self.debug("fail to call get_temp()")
            self.debug(e)
            return ''

        if not force:
            cmd = self.pdffonts + ' ' + self.file._path
            self.debug("cmd", cmd)
            try:
                self.debug("from convert", "OCR?")
                o_ = sub.check_output(cmd, shell=True)

                self.debug("from convert pdffonts")
                self.debug("\n" + o_)

                if o_.count('yes') or o_.count('Type') or o_.count('no'):
                    self.debug('ORC is not necessary!')
                    return self.from_pdf(hero)
            except Exception, e:
                self.debug("* from_pdf_ocr", "looks like OCR is necessary")
                self.debug(e)



        options = [self.pdftopng,
                   self.file._path,
                   os.path.join(self.file._tempdir, 'image')]

        options = ' '.join(options)
        self.debug("from_pdf_ocr", "set options pdftopng:", options)
        try:
            self.debug("from_pdf_ocr", "calling pdftopng")
            sub.call(options, shell=True)
        except Exception, e:
            self.debug("*", "from_pdf_ocr", "fail to use pdftopng")
            self.debug(e)
            return ''

        txt = open(self.txt.path, "w")

        page = 1
        for root, dirs, files in wk.walk(self.file._tempdir, tfiles=['.png']):
            for f in files:
                p_ = os.path.join(root, f.name)
                o_ = os.path.join(root, 'output')
                cmd = [self.tesseract_binary, p_, o_, '-l', 'spa']
                cmd = ' '.join(cmd)
                try:
                    self.debug("from_pdf_ocr", "processing page " + str(page))
                    page += 1
                    sub.call(cmd, shell=True)
                except:
                    self.debug("* from_pdf_ocr", "fail subprocess with", cmd)
                    return ''

                f_ = file(o_ + '.txt', 'r')
                for line in f_:
                    txt.write(line)
                f_.close()
        txt.close()

        try:
            self.debug("from_pdf_ocr", "deleting temp directory", self.file._tempdir)
            sh.rmtree(self.file._tempdir)
        except:
            self.debug("*", "from_pdf_ocr", "fail delete", self.file._tempdir)
            self.debug("*", "from_pdf_ocr", "please remove manually")
        return self.txt.path

    def upper(self):
        if not os.path.exists(self.txt.path):
            self.debug(self.txt.path, "Not Found")
            return self.txt.path

        temp = tmp.NamedTemporaryFile(mode='w', delete=False)

        with open(self.txt.path, 'r') as f:
            for line in f:
                try:
                    line = remove_accents(line)
                except:
                    self.debug("from upper", "fail remove_accents")
                try:
                    line = latin2ascii(line)
                except:
                    self.debug("from upper", "fail latin2ascii")
                try:
                    line = line.encode('ascii', 'replace')
                except:
                    self.debug("from upper", "fail encode(ascii)")
                try:
                    line = line.upper()
                except:
                    self.debug("*", "from upper", "fail .upper()")
                temp.write(line)
            temp.close()
            self.remove_file(self.txt.path)
            try:
                self.debug("moving tempfile", temp.name)
                sh.copy2(temp.name, self.txt.path)
            except:
                self.debug("*", "fail to move tempfile", temp.name)
                self.remove_file(temp.name)
                return ''
        return self.txt.path

    def convert(self, heroes=['xpdf', 'xml'],filepath = '', savein='', overwrite='', uppercase=''):

        self.debug('from convert')


        if filepath.lower().endswith('pdf'):
            return self.from_pdf_ocr(hero=heroes[0],filepath=filepath,savein=savein,overwrite=overwrite,uppercase=uppercase)

        if filepath.lower().endswith('docx'):
            return self.from_docx(hero=heroes[1],filepath=filepath,savein=savein,overwrite=overwrite,uppercase=uppercase)

        if filepath.lower().endswith('doc'):
            return self.from_doc(filepath=filepath,savein=savein,overwrite=overwrite,uppercase=uppercase)

        return "Fail convertion"