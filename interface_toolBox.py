# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMessageBox, QFileDialog
from PyQt4.QtCore import pyqtSlot, QSettings, QObject
import psycopg2
from time import sleep
from PyQt4 import QtGui, uic, QtCore
from campoVirtual import CampoVirtual
from checkEdifIsolada import CheckEdifIsolada
from reindex import Reindex
from checkEdifGeneral import CheckEdifGeneral
import sys, os

sys.path.append(os.path.dirname(__file__))
FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'toolBox.ui'), resource_suffix='')

class InterfaceToolBox(QtGui.QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        super(InterfaceToolBox, self).__init__(parent)
        self.iface = iface
        self.setupUi(self)
        self.progressBar.setRange(0,1)
        self.listConnection()        
    
    def listConnection(self):
        try:
            conf = QSettings()
            conf.beginGroup("PostgreSQL/connections")
            connections=[]
            for x in conf.allKeys():
                if  x[-9:] == "/username":
                    connections.append(x[:-9])
            self.listConnCombo.addItems(connections)
        except:
            QtGui.QMessageBox.warning(self.iface.mainWindow(),"ERRO", u"Erro ao ler 'Conexões'")
    
    def setConnection(self, DB):
        conf = QSettings()
        conf.beginGroup('PostgreSQL/connections')
        host = DB+'/host'
        port = DB+'/port'
        database = DB+'/database'
        username = DB+'/username'
        password = DB+'/password'   
        conn_string = "host="+conf.value(host)+" dbname="+conf.value(database)+\
            " user="+conf.value(username)+" password="+conf.value(password)+" port="+conf.value(port)
        conn = psycopg2.connect(conn_string)
        return conn    
    
    def message(self, msg):
        QMessageBox.warning(self, u"Aviso:", msg, QMessageBox.Close)
        
    def setTask(self, command):
        self._task = command
        
    def taskFinished(self, msg, tipo):
        self.iface.mapCanvas().refresh()
        self.worker.deleteLater()
        self.thread.quit()
        self.thread.wait()
        self.thread.deleteLater()
        self.db.close()
        self.thread = None
        self.worker = None
        self.db = None
        self.progressBar.setRange(0,1)
        if tipo:
            self.progressBar.setValue(1)
        self.startButton.setEnabled(True)
        self.message(msg)
        self.progressBar.setValue(0)
        
    @pyqtSlot(bool)    
    def on_startButton_clicked(self):
        if (not (self.listConnCombo.currentIndex() == 0)) and (self._task != None):
            self.progressBar.setRange(0,0)
            self.startButton.setEnabled(False)
            db = self.setConnection(self.listConnCombo.currentText())
            thread = QtCore.QThread(self)
            worker = self._task(self.iface, db)
            worker.moveToThread(thread)
            worker.finished.connect(self.taskFinished)
            thread.started.connect(worker.run)
            thread.start()
            self.thread = thread
            self.worker = worker
            self.db = db
        else:
            self.message(u'''<font color=red>Campos não definidos:<br></font>
                <font color=blue>Defina todos os campos e tente novamente!</font>''')  
    
    @pyqtSlot(bool)
    def on_reindexButton_clicked(self):
        self.progressBar.reset()
        self.setTask(Reindex)
     
    @pyqtSlot(bool)
    def on_edifGeneralButton_clicked(self):
        self.progressBar.reset()
        self.setTask(CheckEdifGeneral)            
            
    @pyqtSlot(bool)
    def on_edifIsoladaButton_clicked(self):
        self.progressBar.reset()
        self.setTask(CheckEdifIsolada)
                   
    @pyqtSlot(bool)    
    def on_camposVButton_clicked(self):
        self.progressBar.reset()
        self.setTask(CampoVirtual)
        
    

    