import sys, os
from qgis.core import QgsMapLayerRegistry, QgsMapLayer, QgsField, QGis
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtGui import QAction, QIcon
from PyQt4.QtCore import QVariant, QSize
from PyQt4 import QtGui, uic, QtCore
from interface_toolBox import InterfaceToolBox
from campoVirtual import CampoVirtual
import resources

class Main:
    def __init__(self, iface):
        self.iface = iface
       
    def initGui(self):
        self.toolButton = QAction(QIcon(":/plugins/toolBox/icon.png"), u"Caixa de Ferramentas", self.iface.mainWindow())
        self.toolButton.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.toolButton)
        
    def unload(self):    
        pass
            
    def run(self):
        dialog = QtGui.QDialog(self.iface.mainWindow())
        self.d = InterfaceToolBox(self.iface, dialog)
        self.d.show()
   


   
    
    
    