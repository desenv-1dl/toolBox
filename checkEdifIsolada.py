# -*- coding: utf-8 -*-
#imports qgis
from qgis.gui import QgsMessageBar
from qgis.core import QgsDataSourceURI

#imports PyQt
from PyQt4 import QtGui, uic, QtCore, QtSql
from PyQt4.QtCore import QSettings, QObject
from PyQt4.QtCore import pyqtSlot
from PyQt4.Qt import QWidget, QObject, QDialog, QMainWindow


class CheckEdifIsolada(QtCore.QObject):
    finished = QtCore.pyqtSignal(str, int)
    def __init__(self, iface, conn):
        QtCore.QObject.__init__(self)
        self.conn = conn
        self.iface =iface      
 
    def run(self):
        try:
            self.conn.cursor().execute(u"""INSERT INTO "AUX"."Aux_Valida_P" (observacao, geom)
                                                SELECT 'Edificação isolada' as observacao, p.geom 
                                                FROM "public"."view_edificacoes_p" as p 
                                                WHERE id NOT IN ( 
                                                        SELECT distinct b.id 
                                                        FROM "public"."view_edificacoes_p" as b 
                                                        INNER JOIN "TRA"."Trecho_Rodoviario_L" as t ON st_buffer(b.geom, 125) && t.geom 
                                                        WHERE st_intersects(st_buffer(b.geom, 125), t.geom) 
                                                        UNION
                                                        SELECT distinct b.id 
                                                        FROM "public"."view_edificacoes_p" as b 
                                                        INNER JOIN "TRA"."Arruamento_L" as t ON st_buffer(b.geom, 125) && t.geom 
                                                        WHERE st_intersects(st_buffer(b.geom, 125), t.geom)
                                                        UNION
                                                        SELECT distinct b.id 
                                                        FROM "public"."view_edificacoes_p" as b 
                                                        INNER JOIN "TRA"."Trilha_Picada_L" as t ON st_buffer(b.geom, 125) && t.geom 
                                                        WHERE st_intersects(st_buffer(b.geom, 125), t.geom)
                                                ) 
                                                RETURNING id;""")
            self.conn.commit()
            self.conn.cursor().execute(u"""INSERT INTO "AUX"."Aux_Valida_A" (observacao, geom)
                                                SELECT 'Edificação isolada' as observacao, p.geom 
                                                FROM "public"."view_edificacoes_a" as p 
                                                WHERE id NOT IN ( 
                                                        SELECT distinct b.id 
                                                        FROM "public"."view_edificacoes_a" as b 
                                                        INNER JOIN "TRA"."Trecho_Rodoviario_L" as t ON st_buffer(b.geom, 125) && t.geom 
                                                        WHERE st_intersects(st_buffer(b.geom, 125), t.geom)
                                                        UNION
                                                        SELECT distinct b.id 
                                                        FROM "public"."view_edificacoes_a" as b 
                                                        INNER JOIN "TRA"."Arruamento_L" as t ON st_buffer(b.geom, 125) && t.geom 
                                                        WHERE st_intersects(st_buffer(b.geom, 125), t.geom)
                                                        UNION
                                                        SELECT distinct b.id 
                                                        FROM "public"."view_edificacoes_a" as b 
                                                        INNER JOIN "TRA"."Trilha_Picada_L" as t ON st_buffer(b.geom, 125) && t.geom 
                                                        WHERE st_intersects(st_buffer(b.geom, 125), t.geom)
                                                ) 
                                                RETURNING id;""")
            self.conn.commit()
            self.finished.emit(u'<font color=green>Concluído com Sucesso!</font>', 1)
        except:
            self.finished.emit(u'<font color=red>Operação não concluída!</font>', 0)
                
  
   
        
        
        
        
        
        
        
        
        

  
    
    