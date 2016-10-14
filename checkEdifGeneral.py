# -*- coding: utf-8 -*-
#imports qgis
from qgis.gui import QgsMessageBar
from qgis.core import QgsDataSourceURI

#imports PyQt
from PyQt4 import QtGui, uic, QtCore, QtSql
from PyQt4.QtCore import QSettings, QObject
from PyQt4.QtCore import pyqtSlot
from PyQt4.Qt import QWidget, QObject, QDialog, QMainWindow


class CheckEdifGeneral(QtCore.QObject):
    finished = QtCore.pyqtSignal(str, int)
    def __init__(self, iface, conn):
        QtCore.QObject.__init__(self)
        self.conn = conn
        self.iface =iface      
 
    def run(self):
        try:
            self.conn.cursor().execute(u"""INSERT INTO "AUX"."Aux_Valida_L" (observacao, geom)
                                                select 'Edif não generalizada' as observacao, st_multi(geom) as geom
                                                from (
                                                select id, ST_MakeLine(geom, lag(geom) over (partition by id order by path)) as geom
                                                from (
                                                SELECT id, (ST_DumpPoints(geom)).path[3] as path, (ST_DumpPoints(geom)).geom as geom
                                                from public.view_edificacoes_a
                                                ) as foo) as bar
                                                where ST_Length(geom) < 4 and geom IS NOT NULL
                                                RETURNING id;""")
            self.conn.commit()
            self.finished.emit(u'<font color=green>Concluído com Sucesso!</font>', 1)
        except:
            self.finished.emit(u'<font color=red>Operação não concluída!</font>', 0)
                
  
   
        
        
        
        
        
        
        
        
        

  
    
    