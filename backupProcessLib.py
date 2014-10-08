#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan Prieto 
# @Date:   2014-10-07 17:51:15
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2014-10-07 18:16:10

class ProcessLib(QtCore.QThread):
    procDone = QtCore.Signal(bool)
    partDone = QtCore.Signal(int)
    message = QtCore.Signal(str)
    FLAG = True

    def __init__(self, window):
        QtCore.QThread.__init__(self)
        self.window = window

    def debug(self, msg):
        try:
            debug(msg)
            if self.window.checkDebug.isChecked():
                self.message.emit(msg)
                print msg
        except:
            pass

    def run(self):

        self.debug('created QThread for ProcessLib')

        self.window.buttonStart.setEnabled(False)
        self.window.buttonStop.setEnabled(True)


        self.partDone.emit(0)

        try:
            if not os.path.exists(self.window.directory):
                self.debug("Directory does not exist")
        except Exception, e:
            self.debug("Fail review directory of search")
            return

        manager = aTXT()
        conta = 0
        
        for root, dirs, files in wk.walk(
                self.window.directory,
                level=self.window.level,
                tfiles=self.window.tfiles):

            if not self.FLAG:
                self.debug("Process stopped.")
                self.partDone(0)
                self.procDone(True)
                return

            self.debug('Directory: ' + root)

            try:
                if os.path.isdir(self.window.savein):
                    savein = os.path.join(root, self.window.savein)
                else:
                    savein = self.window.savein
            except Exception, e:

                self.debug("Something wrong with savein path: ")
                self.debug(savein)
                self.debug(e)

            try:
                if self.window.clean and os.path.exists(savein):
                    self.debug("Cleaning directory of " + savein)
                    sh.rmtree(savein)
                    self.debug("Remove " + savein + " DONE")
            except Exception, e:
                self.debug("Fail remove " +  savein)

            if self.window.clean:
                continue

            self.debug("Starting process over files in Directory:")

            for f in files:
                conta += 1
                self.debug("File #" + str(conta))
                try:
                    porc = conta*100.0
                    porc /= self.window.totalfiles
                except:
                    porc = 0
                self.partDone.emit(porc)

                filepath = os.path.join(root, f.name)
                
                self.debug('Creating object aTXT class')

                try:
                    self.debug('Conversion started')
                    manager.convert(
                        filepath=filepath,
                        uppercase=self.window.uppercase,
                        overwrite=self.window.overwrite,
                        savein=self.window.savein
                    )

                except Exception, e:
                    self.debug('Fail conversion aTXT calling from GUI.py')
                    self.debug(e)
                    self.debug("*"*50)

        self.debug("Finish Process")
        self.partDone.emit(100)

        self.message.emit("Total Files: " + str(conta))

        try:
            manager.close()
        except Exception, e:
            self.debug("Fail trying to close manager aTXT")
            self.debug(e)
            self.debug("*"*50)

        self.procDone.emit(True)
        self.exit()
        return



class ProcessLib(QtCore.QThread):
    procDone = QtCore.Signal(bool)
    partDone = QtCore.Signal(int)
    message = QtCore.Signal(str)
    FLAG = True

    def __init__(self, window):
        QtCore.QThread.__init__(self)
        self.window = window

    def debug(self, msg):
        try:
            debug(msg)
            if self.window.checkDebug.isChecked():
                self.message.emit(msg)
                print msg
        except:
            pass

    def run(self):

        self.debug('created QThread for ProcessLib')

        self.window.buttonStart.setEnabled(False)
        self.window.buttonStop.setEnabled(True)


        self.partDone.emit(0)

        try:
            if not os.path.exists(self.window.directory):
                self.debug("Directory does not exist")
        except Exception, e:
            self.debug("Fail review directory of search")
            return

        manager = aTXT()
        conta = 0
        
        for filepath in self.window.listfiles:
            if not self.FLAG:
                self.debug("Process stopped.")
                self.partDone(0)
                self.procDone(True)
                return

            if self.window.clean:
                continue


            conta += 1
            self.debug("File #" + str(conta))
            try:
                porc = conta*100.0
                porc /= self.window.totalfiles
            except:
                porc = 0
            self.partDone.emit(porc)
                
            self.debug('Creating object aTXT class')

            try:
                self.debug('Conversion started')
                manager.convert(
                    filepath=filepath,
                    uppercase=self.window.uppercase,
                    overwrite=self.window.overwrite,
                    savein=self.window.savein
                )
            except Exception, e:
                self.debug('Fail conversion aTXT calling from GUI.py')
                self.debug(e)
                self.debug("*"*50)

        self.debug("Finish Process")
        self.partDone.emit(100)

        self.message.emit("Total Files: " + str(conta))

        try:
            manager.close()
        except Exception, e:
            self.debug("Fail trying to close manager aTXT")
            self.debug(e)
            self.debug("*"*50)

        self.procDone.emit(True)
        self.exit()
        return