# -*- coding: utf-8 -*-
from qgis.core import QgsMapLayerRegistry, QgsMapLayer, QgsField, QGis
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QAction, QIcon
from PyQt4.QtCore import QVariant, QSize
    
class CampoVirtual(QtCore.QObject):
    finished = QtCore.pyqtSignal(str, int)
    def __init__(self, iface, conn):
        QtCore.QObject.__init__(self)
        self.iface = iface
                
    def run(self):
        try:
            layers = QgsMapLayerRegistry.instance().mapLayers().values()
            size = len(layers)
            p = 0
            for i in range(size):
                layer = layers[i]
                
                if layer.type() != QgsMapLayer.VectorLayer:
                    continue
                    
                if layer.geometryType() == QGis.Polygon:
                    layer.addExpressionField('$area', QgsField('area_otf', QVariant.Double))
                elif layer.geometryType() == QGis.Line:
                    layer.addExpressionField('$length', QgsField('comprimento_otf', QVariant.Double))
            self.finished.emit(u'<font color=green>Concluído com Sucesso!</font>', 1)
        except:
            self.finished.emit(u'<font color=red>Operação não concluída!</font>', 0)