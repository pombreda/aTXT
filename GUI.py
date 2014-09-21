#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import shutil
from aTXT import aTXT
from version import __version__
import walking as wk
import logging as log
import shutil as sh
import datetime


import locale
import unicodedata
from kitchen.text.converters import getwriter, to_bytes, to_unicode
from kitchen.i18n import get_translation_object

UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

from PySide import QtGui, QtCore

homeDirectory = os.path.expanduser('~')

DEBUG = True

log_filename = "aTXT" + \
    datetime.datetime.now().strftime("-%Y_%m_%d_%H-%M") + ".log"

log.basicConfig(
    filename=log_filename, filemode='w',
    level=log.DEBUG,
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)


def debug(msg, *args):
    if DEBUG:
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


class ProcessLib(QtCore.QThread):
    procDone = QtCore.Signal(bool)
    partDone = QtCore.Signal(int)
    message = QtCore.Signal(str)
    FLAG = True

    def __init__(self, window):
        QtCore.QThread.__init__(self)
        self.window = window

    def run(self):
        debug('created QThread')

        self.window.buttonStart.setEnabled(False)
        self.window.buttonStop.setEnabled(True)

        if self.window.debug:
            cuarentena = os.path.join(self.window.directory, "Files-1KB")
            files_1kb = 0
            try:
                debug("creating folder to files with < 1KB")
                os.makedirs(cuarentena)
                debug("folder created")
            except:
                debug("fail to create", cuarentena)

        msg = 'calling wk.walk to trasverse directories'
        debug(msg)
        self.message.emit(msg)
        self.partDone.emit(0)

        conta = 0
        for root, dirs, files in wk.walk(
                self.window.directory,
                level=self.window.level,
                tfiles=self.window.tfiles):

            if not self.FLAG:
                msg = "Stopped"
                debug(msg)
                self.message.emit(msg)
                return

            msg = 'Looking over ' + root
            debug(msg)
            self.message.emit(msg)

            try:
                if os.path.isdir(self.window.savein):
                    savein = os.path.join(root, self.window.savein)
                else:
                    savein = self.window.savein
            except Exception, e:
                debug("something wrong with savein", savein)
                debug(e)

            try:
                if self.window.clean and os.path.exists(savein):
                    msg = "Cleaning directory of ", savein
                    debug(msg)
                    self.message.emit(msg)
                    shutil.rmtree(savein)
                    msg = "Remove " + savein + " DONE"
                    self.message.emit(msg)
            except Exception, e:
                debug("Fail remove ", savein)

            if self.window.clean:
                continue

            debug("starting process over files:")

            for f in files:
                debug("#file", conta)
                filepath = os.path.join(root, f.name)
                try:
                    msg = "trying to encode utf-8 " + filepath
                    debug(msg)
                    self.message.emit(msg)
                    filepath = to_unicode(filepath,'utf-8')
                except:
                    msg = 'fail to encode filepath'
                    debug(msg)
                    self.message.emit(msg)

                msg = 'creating object aTXT class'
                debug(msg)
                self.message.emit(msg)

                txt = aTXT(
                    filepath=filepath,
                    debug=DEBUG,
                    uppercase=self.window.uppercase,
                    overwrite=self.window.overwrite,
                    savein=self.window.savein
                )

                try:
                    msg = 'conversion started'
                    debug(msg)
                    self.message.emit(msg)

                    txt.convert(heroes=self.window.heroes)
                    msg = 'finish conversion'
                    debug(msg)
                    self.message.emit(msg)

                except Exception, e:
                    debug('fail conversion')
                    debug("error:", e)

                # if self.window.debug:
                #     if os.path.getsize(txt.txt_path) < (1 << 10L):
                #         msg = "file with less of 1KB, " + \
                #             wk.size_str(txt.txt_size())
                #         debug(msg)
                #         self.message.emit(msg)

                #         try:
                #             sh.copy2(txt.txt_path, cuarentena)
                #             sh.copy2(txt.fpath, cuarentena)
                #             files_1kb += 1
                #         except Exception, e:
                #             debug(e)

                self.partDone.emit(conta)
                conta += 1

        msg = "finish processs"
        debug(msg)

        self.partDone.emit(self.window.totalfiles)

        msg = "Total Files: " + str(conta)
        debug(msg)
        self.message.emit(msg)

        if files_1kb > 0:
            try:
                os.rmtree(cuarentena)
            except:
                pass

        self.procDone.emit(True)
        self.exit()
        return


class Window(QtGui.QWidget):
    checked = QtCore.Qt.Checked
    unchecked = QtCore.Qt.Unchecked
    debug = True
    totalfiles = 0
    totalsize = 0

    def __init__(self):
        debug('GUI aTXT v'+__version__+" " +"="*30)
        super(Window, self).__init__()
        debug('set configuration')
        self.config()
        debug('drawing box Directory')
        self.putBoxDirectory()
        debug('drawing box Options')
        self.putBoxOptions()
        self.setLayout(self.layout)

    def config(self):
        self.setWindowTitle("aTXT v." + __version__)

        debug('set size of window',)
        self.setFixedSize(650, 500)

        self.setContentsMargins(15, 15, 15, 15)
        self.layout = QtGui.QVBoxLayout()
        self.layout.addStretch(1)

    def putBoxDirectory(self):
        self.buttonDirectory = QtGui.QPushButton("Browser")
        self.buttonDirectory.clicked.connect(self.findDirectory)
        self.directoryLabel = QtGui.QLineEdit()
        self.directoryLabel.setText(homeDirectory)

        self.directoryLabel.setFixedSize(280, 20)
        self.directoryLabel.setAlignment(QtCore.Qt.AlignRight)

        self.boxDirectoryLayout = QtGui.QGridLayout()
        self.boxDirectoryLayout.addWidget(self.directoryLabel, 0, 1)
        self.boxDirectoryLayout.addWidget(self.buttonDirectory, 0, 0)

        label = QtGui.QLabel()
        label.setText("Level:")

        self.depth_search = QtGui.QSpinBox()
        self.depth_search.setMinimum(0)
        self.depth_search.setMaximum(100)
        # self.depth_search.setValue(1)
        self.depth_search.setFixedSize(50, 25)

        self.boxDirectoryLayout.addWidget(label, 0, 4)
        self.boxDirectoryLayout.addWidget(self.depth_search, 0, 5)

        self.boxDirectory = QtGui.QGroupBox("Directory")
        self.boxDirectory.setLayout(self.boxDirectoryLayout)
        self.layout.addWidget(self.boxDirectory)

    def findDirectory(self):
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        directory = QtGui.QFileDialog.getExistingDirectory(self,
                                                           "QFileDialog.getExistingDirectory()",
                                                           self.directoryLabel.text(), options)
        if directory:
            self.directoryLabel.setText(directory)

    def putBoxOptions(self):
        # TYPE FILES
        self.checkPDF = QtGui.QCheckBox(".pdf")
        self.checkPDF.setCheckState(self.checked)

        self.heroPDF = QtGui.QComboBox()
        self.heroPDF.addItems(['xpdf', 'pdfminer'])

        self.checkDOCX = QtGui.QCheckBox(".docx")
        self.checkDOCX.setCheckState(self.checked)

        self.heroDOCX = QtGui.QComboBox()
        self.heroDOCX.addItems(['xml', 'python-docx'])
        self.checkDOC = QtGui.QCheckBox(".doc")
        self.checkDOC.setCheckState(self.checked)

        if not sys.platform in ["win32"]:
            self.checkDOC.setCheckState(self.unchecked)
            self.checkDOC.setEnabled(False)


        layout = QtGui.QGridLayout()

        layout.addWidget(QtGui.QLabel("Type"), 0, 0)
        layout.addWidget(QtGui.QLabel("Library"), 0, 1)
        layout.addWidget(self.checkPDF, 1, 0)
        layout.addWidget(self.heroPDF, 1, 1)
        layout.addWidget(self.checkDOCX, 2, 0)
        layout.addWidget(self.heroDOCX, 2, 1)
        layout.addWidget(self.checkDOC, 4, 0)

        self.boxTypeFiles = QtGui.QGroupBox("Types Files")
        self.boxTypeFiles.setLayout(layout)

        self.gridSettings = QtGui.QGridLayout()
        self.gridSettings.addWidget(self.boxTypeFiles, 0, 0)

        # SETTINGS
        self.checkUPPER_CASE = QtGui.QCheckBox("Content in Upper Case")

        self.saveinLabel = QtGui.QLabel("Save In:")
        self.saveinLineEdit = QtGui.QLineEdit("TXT")
        self.saveinLineEdit.setFixedSize(100, 20)
        self.saveinLineEdit.setToolTip("aTXT creates new folder\
            for each one that contains files of the search.")

        self.checkOverwrite = QtGui.QCheckBox("Overwrite Files")
        self.checkOverwrite.setToolTip(
            "If there the .txt version of file, don't proccess file again with aTXT")
        self.checkOverwrite.setCheckState(self.checked)
        # debug
        self.checkClean = QtGui.QCheckBox("Clean Directory")
        self.checkClean.setToolTip("Remove Directories with name above enter")
        self.checkClean.setCheckState(self.unchecked)

        self.checkDebug = QtGui.QCheckBox("Debug")
        self.checkDebug.setCheckState(self.checked)

        layout = QtGui.QGridLayout()
        layout.addWidget(self.checkOverwrite, 0, 0)
        layout.addWidget(self.checkUPPER_CASE, 1, 0)
        layout.addWidget(self.saveinLabel, 3, 0)
        layout.addWidget(self.saveinLineEdit, 3, 1)
        layout.addWidget(self.checkClean, 5, 0)
        layout.addWidget(self.checkDebug, 5, 1)

        self.boxSettings = QtGui.QGroupBox("Settings")
        self.boxSettings.setLayout(layout)

        self.gridSettings.addWidget(self.boxSettings, 0, 1)
        self.layout.addLayout(self.gridSettings)

        # DETAILS

        self.progress_bar = QtGui.QProgressBar()
        frameStyle = QtGui.QFrame.Sunken | QtGui.QFrame.Panel
        self.current_process = QtGui.QTextEdit()
        self.current_process.setEnabled(False)
        self.current_process.setFrameStyle(frameStyle)

        self.boxDetails = QtGui.QGroupBox("Details")

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.current_process)
        self.boxDetails.setLayout(layout)
        self.boxDetails.setEnabled(False)
        self.layout.addWidget(self.boxDetails)

        # ACTIONS
        self.buttonReset = QtGui.QPushButton("Reset")
        self.buttonReset.clicked.connect(self.resetOptions)

        self.buttonScan = QtGui.QPushButton("Scan")
        self.buttonScan.clicked.connect(self.scanDir)

        self.buttonStop = QtGui.QPushButton("Stop")
        self.buttonStop.setEnabled(False)
        self.buttonStop.clicked.connect(self.stopProcess)

        self.buttonStart = QtGui.QPushButton("Execute")
        self.buttonStart.setEnabled(False)
        self.buttonStart.clicked.connect(self.startProcess)

        box = QtGui.QGroupBox("Actions")
        layout = QtGui.QGridLayout()
        layout.setColumnStretch(1, 1)
        layout.addWidget(self.buttonReset, 0, 0)
        layout.addWidget(self.buttonScan, 0, 1)
        layout.addWidget(self.buttonStop, 0, 5)
        layout.addWidget(self.buttonStart, 0, 6)
        box.setLayout(layout)
        self.layout.addWidget(box)

    def resetOptions(self):
        self.setEnabled(True)
        self.directoryLabel.setText(homeDirectory)
        self.depth_search.setValue(0)
        self.setProgress(0)
        self.checkPDF.setCheckState(self.checked)
        self.checkDOCX.setCheckState(self.checked)

        self.checkDOC.setCheckState(self.checked)
        if not sys.platform in ["win32"]:
            self.checkDOC.setCheckState(self.unchecked)
            self.checkDOc.setEnabled(False)
            
        self.checkOverwrite.setCheckState(self.checked)
        self.saveinLineEdit.setText("TXT")
        self.checkClean.setCheckState(self.unchecked)
        self.checkDebug.setCheckState(self.checked)
        self.checkUPPER_CASE.setCheckState(self.unchecked)
        self.buttonStart.setEnabled(False)
        self.buttonStop.setEnabled(False)
        self.current_process.setText("")
        return

    def scanDir(self):
        debug("")
        debug("from scanDir", "starting scanning")
        self.progress_bar.setValue(0)

        self.directory = self.directoryLabel.text()
        try:
            debug('trying to encode utf-8 directory name')
            self.directory = to_unicode(self.directory,'utf-8')
        except:
            debug('fail to encode')

        debug("directory:", self.directory)

        self.level = self.depth_search.text()
        try:
            debug('casting to int of level definition')
            self.level = int(self.level)
        except:
            debug('fail casting level')

        debug("level:", self.level)

        self.tfiles = []
        if self.checkPDF.isChecked():
            self.tfiles.append('.pdf')
        if self.checkDOCX.isChecked():
            self.tfiles.append('.docx')
        if self.checkDOC.isChecked():
            self.tfiles.append('.doc')
        debug("tfiles:", self.tfiles)

        self.setStatus('Calculating the total size of files ...')
        self.totalfiles, self.totalsize = [0] * 2

        if len(self.tfiles) > 0:
            debug('starting scanning in directory, calling wk.walk_size')
            try:
                self.totalfiles, self.totalsize = wk.walk_size(
                    self.directory, [], self.level, self.tfiles)
            except Exception, e:
                debug("something was wrong with wk.walk_size")
                debug(e)
                debug("review arguments: ", self.directory,
                      [], self.level, self.tfiles)

        s = "{0} file(s) with total size of {1}".format(
            self.totalfiles, wk.size_str(self.totalsize))

        self.setStatus(s)

        debug("totalfiles:", self.totalfiles)
        debug("totalsize:", wk.size_str(self.totalsize))

        debug("Options:")
        self.savein = self.saveinLineEdit.text()
        try:
            debug("trying to encode utf-8")
            self.savein = to_unicode(self.savein, 'utf-8')
        except:
            debug('fail encode utf-8')
        debug('savein:', self.savein)

        self.heroes = [self.heroPDF.currentText(), self.heroDOCX.currentText()]
        debug('heroes: ', self.heroes)

        debug('debug: ', self.debug)

        self.clean = self.checkClean.isChecked()
        debug('clean: ',  self.clean)

        self.uppercase = self.checkUPPER_CASE.isChecked()
        debug("uppercase: ",  self.uppercase)

        self.overwrite = self.checkOverwrite.isChecked()
        debug('overwrite: ',  self.overwrite)

        if self.totalfiles > 0:
            debug('Ready to start conversion')
            debug('')
            self.buttonStart.setEnabled(True)
        self.setEnabled(False)
        return

    def stopProcess(self):
        try:
            self.thread.FLAG = False
            self.thread.terminate()
            if self.thread.isRunning():
                self.stopProcess()
                return
            self.buttonStop.setEnabled(False)
            self.buttonScan.setEnabled(True)
            self.buttonReset.setEnabled(True)
            self.boxDetails.setEnabled(True)
            self.progress_bar.setEnabled(False)
            # self.resetOptions()
        except:
            pass
        self.setEnabled(True)
        self.tfiles = []
        return

    def startProcess(self):
        if len(self.tfiles) == 0:
            self.buttonStart.setEnabled(False)
            return
        self.thread = ProcessLib(self)
        self.thread.partDone.connect(self.setProgress)
        self.thread.procDone.connect(self.fin)
        self.thread.message.connect(self.setStatus)
        self.buttonStop.setEnabled(True)
        self.buttonScan.setEnabled(False)
        self.buttonReset.setEnabled(False)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(self.totalfiles)
        self.thread.start()
        self.setEnabled(False)
        return

    def setEnabled(self, value):
        self.boxDirectory.setEnabled(value)
        self.boxSettings.setEnabled(value)
        self.boxTypeFiles.setEnabled(value)
        return

    def setStatus(self, menssage):
        if self.checkDebug.isChecked():
            self.current_process.append(menssage)
        else:
            self.current_process.setText(menssage)
        self.current_process.moveCursor(QtGui.QTextCursor.End)

    def setProgress(self, value):
        if value > 100:
            value = 100
        self.progress_bar.setValue(value)

    def fin(self):
        self.progress_bar.reset()
        self.stopProcess()


def main():
    app = QtGui.QApplication(sys.argv)
    wds = Window()
    wds.show()
    sys.exit(app.exec_())
    del wds

if __name__ == "__main__":
    main()
