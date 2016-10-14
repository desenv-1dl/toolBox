# -*- coding: utf-8 -*-
#imports system
import os
import sys

#imports qgis
from qgis.gui import QgsMessageBar
#imports PyQt
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import QSettings, QObject
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtSql import QSqlDatabase
from PyQt4.Qt import QWidget, QObject

class Reindex(QtCore.QObject):
    finished = QtCore.pyqtSignal(str, int)
    def __init__(self, iface, conn):         
        QtCore.QObject.__init__(self)
        self.conn = conn
        self.iface =iface 
    
    def run(self):
        try:
            if self.iface.activeLayer():
                dataExtra = self.iface.activeLayer().styleURI()
                table = dataExtra.split(' ')[-3][6:]
                self.conn.cursor().execute("""SELECT setval('%s_id_seq"', 1+(SELECT max(id) from %s),false);""" %(table[:-1], table))
                self.conn.cursor().close()
                self.finished.emit(u'<font color=green>Concluído com Sucesso!</font>', 1)
            else:
                self.finished.emit(u'<font color=red>Operação não concluída:<br/>Não há feições ativas!</font>', 0)
        except:
            self.finished.emit(u'<font color=red>Operação não concluída!</font>', 0)
            
  
