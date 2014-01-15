#!/usr/bin/env python
# d555
# Jonathan Prieto

import sys
import os
import re
import errno
import shutil

# conversion desde docx
from docx import opendocx, getdocumenttext
# conversion desde pdf
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter

# PATRONES -> se puede remplazar con endswith
patronDocx = re.compile(".*\.docx$")
patronPDF = re.compile(".*\.pdf$")
patronDir = re.compile(".*/TXT")
patronDoc = re.compile("[^~].*\.doc$")

def doc2TXT(path, nombre_archivo):
	'''
		Este metodo solo funciona en win
		con el paquete de ofimatica office -word-
		dado que hace uso de un Dispatch con word
	'''

	DIR = path + "/TXT"
	crear_directorio( DIR )
	nuevo_nombre = ""
	try:
		import win32com.client
		w = win32com.client.Dispatch("Word.Application")
		w.visible = 0
		archivo = path + "/" + nombre_archivo
		
		wb = w.Documents.Open(archivo)
		nuevo_nombre = nombre_archivo.split(".")[0] + ".txt"
		nuevo = DIR + "/"  + nuevo_nombre
		#wb.SaveAs(res, FileFormat = 12)
		wb.SaveAs(nuevo, FileFormat = 2 )
		wb.Close()
		w.Quit()
		return [True, nuevo_nombre]
	except:
		print "Error en doc2TXT()"
		return [False, nuevo_nombre]


def crear_directorio(path):
	try:
		os.makedirs(path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise

def docx2TXT(path, nombre_archivo):
	DIR =  path + "/TXT"
	crear_directorio( DIR )
	try:
		documento = opendocx(path + "/" + nombre_archivo)
		nuevo_nombre = nombre_archivo.split(".")[0] + ".txt"
		nuevo = open(DIR + "/" + nuevo_nombre, "w")
	except:
		return [False, "ocurrio un problema!!"]
	paratextlist = getdocumenttext(documento)
	newparatextlist = []
	for paratext in paratextlist:
		newparatextlist.append(paratext.encode("utf-8"))
	nuevo.write('\n\n'.join(newparatextlist))
	nuevo.close()
	return [True,nuevo_nombre]

def pdf2TXT(path, nombre_archivo):
	DIR =  path + "/TXT"
	crear_directorio( DIR )
	nuevo_nombre = nombre_archivo.split(".")[0] + ".txt"
	# opciones para pdfminer...
	password = ''
	pagenos = set()
	maxpages = 0
	# output option
	outfile = nuevo_nombre
	outtype = "text"
	imagewriter = None
	layoutmode = 'normal'
	codec = 'utf-8'
	pageno = 1
	scale = 1
	caching = True
	showpageno = True
	laparams = LAParams()

	rsrcmgr = PDFResourceManager(caching=caching)
	outfp = open(DIR + "/" + nuevo_nombre, "w")
	device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
							   imagewriter=imagewriter)
	fname = path + "/" + nombre_archivo
	fp = open(fname, 'rb')
	interpreter = PDFPageInterpreter(rsrcmgr, device)
	for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
		interpreter.process_page(page)
	fp.close()
	device.close()
	outfp.close()
	return [True, nuevo_nombre]

def main(argv):
	import getopt
	def usage():
		print (
		'********\naTXT v.01\n'
		'Extractor de texto\n' 
		'Generacion de archivos de texto \".txt\" de archivos \".docx\" o \".pdf\"\n'
		'en lo profundo de un directorio, sobre subdirectorios.\n'
		'mail: prieto.jona@gmail.com\n'
		'********\n\n'
		'Nota: Sobre el directorio raiz (opcion -p) se crea una carpeta \"TXT\"\nen cada subdirectorio donde se encuentre archivos  \".docx\" o \".pdf\"\ndependiendo de las opciones que el usuario quiera.\n\n'
		'modo de uso: python {0} [opciones ...]\n'
		'-p path_dir\tEspecifica el folder donde se ejecuta la busqueda y conversion de archivos\n'
		'--docx\t\tConvertir archivos en Microsoft Office .docx a .txt\n'
		'--doc\t\tConvertir archivos en Microsoft Office .doc a .txt\n'
		'--pdf\t\tConvertir archivos en formato PDF .txt\n'
		'-l\t\tRegistros generados\n'
		'-b\t\tBorrar toda subdirectorio \"TXT\" en el directorio raiz\n'
		'-d\t\tImprimir directorios relevantes\n\n'
		'-h\t\tImprimir ayuda\n\n'
		'ejemplo de uso: \npython {0} --pdf --docx -l'
		 ).format( argv[0])
		exit()
	dirname, filename = os.path.split(os.path.abspath(__file__))
	if len(argv) > 1:
		try:
			(opts, args) = getopt.getopt(argv[1:], 'p:ldb', ['docx', 'pdf', 'verlog'])
		except getopt.GetoptError:
			usage()
		db = False
		log = False
		DOCX = False
		PDF = False
		borrarTXT = False
		# if not args: return usage()
		for (k, v) in opts:
			if k == '-d': db = True
			elif k == '-l': log = True
			elif k == '-p': dirname = str(v)
			elif k == '-b': borrarTXT = True
			elif k == '--docx': DOCX = True
			elif k == '--doc': DOC = True
			elif k == '--pdf': PDF = True
			elif k == '-h':
				usage()

		if not DOCX and not PDF and not borrarTXT:
			usage()
	else:
        # FRANCISCO
		db = True
		log = True
		DOCX = True
		DOC = True
		PDF = True
		borrarTXT = False

	dirs_afectados = []
	cantidad_docx = 0
	cantidad_doc = 0
	cantidad_pdf = 0
	if not borrarTXT:
		arhivos_procesados = []
		for path, dirs, files in os.walk(dirname):
			for archivo  in files:
				nombre_dir = path.split(dirname)[1]
				if nombre_dir == "": nombre_dir = "/"
				entro = False
				if DOCX and patronDocx.match(archivo):
					proceso = docx2TXT(path, archivo)
					cantidad_docx =  cantidad_docx + 1
					entro = True
				elif DOC and patronDoc.match(archivo):
					proceso = doc2TXT(path, archivo)
					cantidad_doc = cantidad_docx + 1
					entro = True
				elif PDF and patronPDF.match(archivo):
					proceso = pdf2TXT(path, archivo)
					cantidad_pdf = cantidad_pdf + 1
					entro = True
				if entro:
					if nombre_dir  not in dirs_afectados:
						dirs_afectados.append(nombre_dir)
					if proceso[0]:
						arhivos_procesados.append("{0}/{1}".format(path,archivo))
						if db : 
							print "[0k] {0}/{1}".format(path,archivo)

		if log:
			print "En: ", dirname
			i = 1
			for dir in dirs_afectados:
				print "[{0}] {1}".format(i, dir)
				i = i + 1
			print "Total txts creados: {0}".format(len(arhivos_procesados))
			print "\t - doc:", cantidad_doc
			print "\t - docx:", cantidad_docx
			print "\t - pdfs:", cantidad_pdf
			print "Total Directorios TXT Creados: ", len(dirs_afectados)
	elif borrarTXT:
		print "Borrando directorios TXT "
		for path, dirs, files in os.walk(dirname):
			if patronDir.match(path):
				print path.split(dirname)[1]
				try:
					shutil.rmtree(path)
					if db or l:	print "borrado> {0}".format(path)
				except:
					pass
	print "\n\n Pulse cualquier tecla para finalizar.\n"
	a = raw_input()	

if __name__ == '__main__': sys.exit(main(sys.argv))