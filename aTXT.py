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

import sys
import subprocess as sub
import shutil as sh
import logging as log
import zipfile as zp
import datetime
try:
    from win32com import client
    
except:
    pass

import locale
import unicodedata
from kitchen.text.converters import getwriter, to_bytes, to_unicode
from kitchen.i18n import get_translation_object

UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)



from latin2ascii import latin2ascii, remove_accents

log_filename = "aTXT" + \
    datetime.datetime.now().strftime("-%Y_%m_%d_%H-%M") + ".log"


class aTXT(object):

    def __init__(self,
                 filepath='',
                 debug=False,
                 verbose=False,
                 lang='spa',
                 overwrite=True,
                 uppercase=False,
                 savein='TXT',
                 msword=None):

        self.debug = debug
        self.log_path = log_filename

        if self.debug:
            log.basicConfig(filename=self.log_path, filemode='w',
                            level=log.DEBUG,
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p'
                            )

        self.verbose = verbose
        if self.verbose:
            log.basicConfig(level=log.DEBUG,
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

        self._debug("aTXT v" + __version__ + "=" * 30)
        self.lang = lang
        self._debug('File info:')
        self.fpath = filepath
        # try:
        #     self._debug('trying to encode utf-8 filepath')
        #     self.fpath = self.fpath.encode('utf-8')
        # except:
        #     self._debug('fail to encode')

        self._debug('\tpath:', self.fpath)
        if not os.path.exists(self.fpath):
            self._debug("In", self.fpath, "file not found")

        self.fbasename = os.path.basename(filepath)
        self._debug('\tbasename:', self.fbasename)

        self.fname, self.fext = os.path.splitext(self.fbasename)
        self.foverwrite = overwrite
        self._debug('\toverwrite:', self.foverwrite)

        self.fuppercase = uppercase
        self._debug('\tuppercase:', self.fuppercase)

        self.fdir = os.path.dirname(filepath)
        self._debug("\tsize:", wk.size_str(self.fsize()))

        self._debug('txt file:')
        self.txt_name = self.fname
        if self.fuppercase:
            self.txt_name = self.txt_name.upper()

        self.txt_basename = self.txt_name + ".txt"
        self._debug('\tbasename:', self.txt_basename)

        self.savein = savein
        if savein == "TXT" or not savein or \
           not os.path.isdir(savein) or \
           not os.path.exists(savein):
            self.savein = os.path.join(self.fdir, "TXT")

        # try:
        #     self._debug('trying to encode utf-8 savein')
        #     self.savein = to_unicode(self.savein.encode,'utf-8')
        #     self._debug('savein', self.savein)

        # except:
        #     self._debug('fail to encode utf-8')

        self.txt_path = os.path.join(self.savein, self.txt_basename)
        self._debug('\tpath:', self.txt_path)
        self._debug('Ready to start conversion!')
        self._debug('')

        self.tesseract_required = "3.02.02"
        self.xpdf_required = "3.04"

        if sys.platform in ["win32"]:
            self._debug('set thirdy paths for win32')
            try:
                self.xpdf_path = os.path.join(os.curdir, 'bin', 'win', 'bin64')
                self.pdftotext = os.path.join(self.xpdf_path, 'pdftotext.exe')
                self.pdftopng = os.path.join(self.xpdf_path, 'pdftopng.exe')
                self.pdffonts = os.path.join(self.xpdf_path, 'pdffonts.exe')
            except:
                self._debug('fail set thirdy paths for win32')

        elif sys.platform in ["darwin"]:
            self._debug('set thirdy paths for darwin mac')
            try:
                self.xpdf_path = os.path.join(os.curdir, 'bin', 'mac', 'bin64')
                self.pdftotext = os.path.join(self.xpdf_path, 'pdftotext')
                self.pdftopng = os.path.join(self.xpdf_path, 'pdftopng')
                self.pdffonts = os.path.join(self.xpdf_path, 'pdffonts')
            except:
                self._debug('fail set thirdy paths for darwin mac')

        if not os.path.exists(self.pdftotext):
            self._debug("not exists", self.pdftotext)
        if not os.path.exists(self.pdftopng):
            self._debug("not exists", self.pdftopng)

        self._debug('set path for tesseract OCR')

        if str(os.name) == 'nt':
            self.tesseract_binary = '"c:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"'
        else:
            self.tesseract_binary = "/usr/local/bin/tesseract"
            if self.debug:
                try:
                    self._debug(
                        "trying to find tesseract binary by which command")
                    self.tesseract_binary = sub.check_output(
                        ['which', 'tesseract']).rstrip()
                except:
                    self._debug("*", "fail with which commnand")
                self._debug("set tesseract: ", self.tesseract_binary)

        self._debug("TEMP", "creating temp directory")
        self.tempdir = tmp.mkdtemp()

        self._debug("dir created", self.tempdir)
        try:
            self._debug("from_pdf_ocr", "copy ", self.fname, "to ", self.tempdir)
            sh.copy2(self.fpath, self.tempdir)
        except:
            self._debug("* fail to copy of", self.fbasename, "to", self.tempdir)

        self.temp_name = "temp" 
        self.temp_basename = self.temp_name + self.fext
        self.temp_path = os.path.join(self.tempdir, self.temp_basename)
        try:
            self._debug("change name for secure process to "+self.temp_basename)
            os.rename(os.path.join(self.tempdir, self.fbasename), self.temp_path)
        except Exception, e:
            self._debug("fail to change name to 1.pdf", e)
        self.msword = msword


    def _debug(self, msg, *args):
        if self.debug:
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

    def make_dir(self, dir):
        try:
            os.makedirs(dir)
            self._debug('Directory created:', dir)
        except:
            self._debug("*", 'fail creating directory,maybe exists ', dir)
        if not os.access(dir, os.W_OK):
            self._debug('Directory without permissions: %s' % dir)
            return 0
        return 1

    def remove_dir(self, dir):
        if os.path.isdir(dir):
            try:
                sh.rmtree(dir)
                self._debug("Directory removed", dir)
                return 1
            except:
                self._debug("*", "Failed remove directory", dir)
        return 0

    def remove_file(self, filepath):
        if os.path.isfile(filepath):
            try:
                sh.remove(filepath)
                self._debug("File deleted", filepath)
                return 1
            except:
                self._debug("*", "Failed remove file", filepath)
        return 0

    def txt_remove(self):
        return self.remove_file(self.txt_path)

    def fsize(self, path=''):
        if not path:
            path = self.fpath
        if not os.path.exists(path):
            self._debug("not exists file", path)
            return 0
        if not os.path.isfile(path):
            self._debug("is not a file", path)
            return 0
        size = os.path.getsize(path)
        self._debug("Size:", wk.size_str(size))
        return size

    def txt_size(self):
        return self.fsize(path=self.txt_path)

    def move(self, topath=''):
        if not topath:
            topath = self.txt_path
        if not self.foverwrite and \
                os.path.exists(os.path.join(topath, self.fbasename)):
            return self.txt_path
        try:
            self._debug("moving from", self.fpath, "to", topath)
            sh.copy2(self.fpath, topath)
            self._debug("file moved")
        except Exception, e:
            self._debug("*", "fail moving file", e)
        return topath

    def from_doc(self):
        # TODO: assert fext is accurate
        self._debug('starting doc to txt')
        try:
            assert os.path.isfile(self.temp_path)
        except:
            self._debug("*", "from_doc", self.temp_path, "is not a file")
            return ''

        try:
            if not os.path.exists(self.savein):
                self.make_dir(self.savein)
        except:
            self._debug("*", "from_doc", self.savein, "review folder")

        if not self.foverwrite and os.path.exists(self.txt_path):
            self._debug(self.txt_path, "yet exists")
            return self.txt_path


        try:
            self._debug("from_doc", "dispatching word")
            # w = win32com.client.Dispatch("Word.Application")
            # w.visible = 0
            cerrar = False
            if not self.msword:
                self.msword = client.DispatchEx("Word.Application") # Using DispatchEx for an entirely new Word instance
                self.msword.Visible = True
                cerrar = True

            try:
                self._debug("from_doc", "opening file", self.temp_path)
                # wb = self.msword.Documents.Open(self.temp_path)

                # http://msdn.microsoft.com/en-us/library/bb216319%28office.12%29.aspx
                # wb = self.msword.Documents.OpenNoRepairDialog(
                wb = self.msword.Documents.Open(
                    FileName = self.temp_path, 
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
                    Visible = True, 
                    # OpenConflictDocument, 
                    OpenAndRepair = True, 
                    # DocumentDirection, 
                    NoEncodingDialog = True
                    )

            except Exception, e:
                self._debug("from_doc", "fail open file with Word", e)
            try:
                self._debug("from_doc", "saving file", self.txt_path)
                wb.SaveAs(self.txt_path, FileFormat=2)
            except Exception, e:
                self._debug("from_doc", "fail to save file", e)

            self._debug("from_doc", "closing file")
            wb.Close()
            self._debug("from_doc", "closing word office")
            if cerrar:
                self.msword.Quit()
            return self.txt_path
        except Exception, e:
            self._debug("*", "from_doc", "fail Dispatch word", e)
            self._debug("*", "from_doc", "removing ", self.txt_path)
            self.remove_file(self.txt_path)
        return ''

    def from_docx(self, hero="python-docx"):
        # TODO: assert fext is accurate

        self._debug('starting docx to txt')
        try:
            assert os.path.isfile(self.temp_path)
        except:
            self._debug("*", "from_docx", self.temp_path, "is not a file")
            return "0"

        try:
            if not os.path.exists(self.savein):
                self.make_dir(self.savein)
        except:
            self._debug("*", "from_docx", self.savein, "review folder")

        if not self.foverwrite and os.path.exists(self.txt_path):
            self._debug(self.txt_path, "yet exists")
            return self.txt_path

        try:
            self._debug("from_docx", "creating file", self.txt_path)
            self.txt_doc = open(self.txt_path, "w")
            self._debug("from_docx", "file created", self.txt_path)
        except:
            self._debug("*", "from_docx", "fail to create", self.txt_path)
            return ''

        self._debug('from_docx', 'hero =', hero)
        if hero == "python-docx":
            self._debug('from_docx', 'starting python-docx')
            doc_ = docx.opendocx(self.temp_path)
            for line in docx.getdocumenttext(doc_):
                try:
                    line = latin2ascii(unicode(line, 'utf-8', 'ignore'))
                except:
                    pass
                try:
                    line = line.encode('utf-8', 'replace')
                except:
                    pass
                self.txt_doc.write(line + '\n')
            self.txt_doc.close()
            return self.txt_path
        try:
            self.txt_doc.write(self.from_docx_())
        except Exception, e:
            self._debug("*", 'from_docx_ error', e)
            return ''
        return self.txt_path

    def from_docx_(self):
        # TODO: assert fext is accurate
        '''
         http://stackoverflow.com/questions/42482/best-way-to-extract-text-from-a-word-doc-
         without-using-com-automation
        '''
        try:
            from xml.etree.cElementTree import XML
        except:
            self._debug("*", "from_docx_ failed XML")
            from xml.etree.ElementTree import XML

        WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
        PARA = WORD_NAMESPACE + 'p'
        TEXT = WORD_NAMESPACE + 't'

        document = zp.ZipFile(self.temp_path)

        self._debug("from_docx_ zipfile open document")
        xml_content = document.read('word/document.xml')

        self._debug("from_docx_ close document")
        document.close()

        self._debug("from_docx_ XML(xml_content)")
        tree = XML(xml_content)
        paragraphs = []

        self._debug("from_docx_ tree.iterator")
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

    def from_pdf(self, hero="xpdf"):
        # TODO: assert fext is accurate

        self._debug('starting pdf to txt')
        try:
            assert os.path.isfile(self.temp_path)
        except:
            self._debug("*", "from_pdf", self.temp_path, "is not a file")
            return ''
        try:
            if not os.path.exists(self.savein):
                self.make_dir(self.savein)
        except:
            self._debug("*", "from_pdf", self.savein, "review folder")

        if not self.foverwrite and os.path.exists(self.txt_path):
            self._debug(self.txt_path, "yet exists")
            return self.txt_path

        try:
            self._debug("from_pdf", "opening to read", self.temp_path)
            doc_ = file(self.temp_path, 'rb')
        except Exception, e:
            self._debug("*", "from_pdf", e)
            return ''
        try:
            self._debug("from_pdf", "creating to write", self.txt_path)
            self.txt_doc = file(self.txt_path, "wb")
            self._debug("from_pdf created", self.txt_basename)
        except Exception, e:
            self._debug("*", "from_pdf", e)
            return ''

        if hero == "pdfminer":
            try:
                self._debug("from_pdf", "creating PDFResourceManager")
                resourceman = pdfinterp.PDFResourceManager()
                self._debug("from_pdf",  "using TextConverter")
                device = converter.TextConverter(
                    resourceman, self.txt_doc, laparams=layout.LAParams())
                self._debug("from_pdf",  "using PDFPageInterpreter")
                interpreter = pdfinterp.PDFPageInterpreter(resourceman, device)
                for page in pdfpage.PDFPage.get_pages(doc_):
                    interpreter.process_page(page)
                self.txt_doc.close()
                device.close()
            except Exception, e:
                self._debug("*", "from_pdf", e)
                return ''

        if hero == "xpdf":
            try:
                self._debug("from_pdf", "xpdf")
                try:
                    options = [self.pdftotext, unicode(self.temp_path), '-']
                except:
                    options = [self.pdftotext, self.temp_path, '-']

                self._debug("from_pdf", options)

                self._debug("from_pdf", "starting subprocess")
                output = sub.call(options, stdout=self.txt_doc)
                self._debug("from_pdf", "finisehd subprocess")
                if output == 0:
                    self._debug("from_pdf", "No error.")
                elif output == 1:
                    self._debug("from_pdf", "Error opening a PDF file.")
                elif output == 2:
                    self._debug("from_pdf", "Error opening an output file.")
                elif output == 3:
                    self._debug(
                        "from_pdf", "Error related to PDF permissions.")
                else:
                    self._debug("from_pdf", "Other error.")
            except Exception, e:
                self._debug("*", "from_pdf", e)
        self.txt_doc.close()
        doc_.close()
        return self.txt_path

    def from_pdf_ocr(self, hero="xpdf",force=False):
        self._debug('starting from_pdf_ocr')
        try:
            assert os.path.isfile(self.temp_path)
        except:
            self._debug("*", "from_pdf_ocr", self.temp_path, "is not a file")
            return ''
        try:
            if not os.path.exists(self.savein):
                self.make_dir(self.savein)
        except:
            self._debug("*", "from_pdf_ocr", self.savein, "review folder")

        if not self.foverwrite and os.path.exists(self.txt_path):
            self._debug(self.txt_path, "yet exists")
            return self.txt_path

        if not force:
            cmd = self.pdffonts + ' ' + self.temp_path

            self._debug("cmd", cmd)
            try:
                self._debug("from convert", "OCR?")
                o_ = sub.check_output(cmd, shell=True)

                self._debug("from convert pdffonts")
                # self._debug("\n" + o_)
                self._debug(o_.count('yes'))
                self._debug(o_.count('Type'))
                self._debug(o_.count('no'))

                if o_.count('yes') or o_.count('Type') or o_.count('no'):
                    self._debug('ORC is not necessary!')
                    return self.from_pdf(hero)
                    # if self.txt_size() > (1<<2L):
                    #     return newfile
                    # return self.from_pdf_ocr(hero=hero, force=True)
            except:
                self._debug("*", "from convert", "looks like OCR is necessary")

        options = [self.pdftopng,
                   self.temp_path,
                   os.path.join(self.tempdir, 'image')]
        options = ' '.join(options)
        self._debug("from_pdf_ocr", "set options pdftopng:", options)
        try:
            self._debug("from_pdf_ocr", "calling pdftopng")
            sub.call(options, shell=True)
            # sub.call('open '+tpath, shell=True)
        except:
            self._debug("*", "from_pdf_ocr", "fail to use pdftopng")
            return ''

        self._debug("from_pdf_ocr", "creating temp txt")
        txt = tmp.NamedTemporaryFile(dir=self.tempdir, delete=False)
        self._debug("from_pdf_ocr", "created txt", txt.name)
        page = 1
        for root, dirs, files in wk.walk(self.tempdir, tfiles=['.png']):
            for f in files:
                p_ = os.path.join(root, f.name)
                o_ = os.path.join(root, 'output')
                cmd = [self.tesseract_binary, p_, o_, '-l', 'spa']
                cmd = ' '.join(cmd)
                try:
                    self._debug("from_pdf_ocr", "processing page " + str(page))
                    page += 1
                    sub.call(cmd, shell=True)
                except:
                    self._debug(
                        "*", "from_pdf_ocr", "fail subprocess with", cmd)
                    return ''

                f_ = file(o_ + '.txt', 'r')
                for line in f_:
                    txt.write(line)
                f_.close()
        txt.close()
        try:
            self._debug(
                "from_pdf_ocr", "rename ", txt.name, "to", self.txt_basename)
            os.rename(txt.name, self.txt_path)
        except:
            self._debug("*", "from_pdf_ocr", "fail rename")
            return ''

        try:
            self._debug("from_pdf_ocr", "deleting temp directory", self.tempdir)
            sh.rmtree(self.tempdir)
        except:
            self._debug("*", "from_pdf_ocr", "fail delete", self.tempdir)
            self._debug("*", "from_pdf_ocr", "please remove manually")

        return self.txt_path

    def upper(self):
        if not os.path.exists(self.txt_path):
            self._debug(self.txt_path, "Not Found")
            return self.txt_path

        temp = tmp.NamedTemporaryFile(mode='w', delete=False)

        with open(self.txt_path, 'r') as f:
            for line in f:
                try:
                    line = remove_accents(line)
                except:
                    self._debug("from upper", "fail remove_accents")
                try:
                    line = latin2ascii(line)
                except:
                    self._debug("from upper", "fail latin2ascii")
                try:
                    line = line.encode('ascii', 'replace')
                except:
                    self._debug("from upper", "fail encode(ascii)")
                try:
                    line = line.upper()
                except:
                    self._debug("*", "from upper", "fail .upper()")
                temp.write(line)
            temp.close()
            self.remove_file(self.txt_path)
            try:
                self._debug("moving tempfile", temp.name)
                sh.copy2(temp.name, self.txt_path)
            except:
                self._debug("*", "fail to move tempfile", temp.name)
                self.remove_file(temp.name)
                return ''
        return self.txt_path

    def txt_open(self):
        return file(self.txt_path, "r")

    def convert(self, heroes=['xpdf', 'xml']):
        self._debug('converting...')

        if self.fext.lower().endswith('pdf'):
            return self.from_pdf_ocr(heroes[0])

        if self.fext.lower().endswith('docx'):
            return self.from_docx(heroes[1])

        if self.fext.lower().endswith('doc'):
            return self.from_doc()

        return "Fail convertion"
