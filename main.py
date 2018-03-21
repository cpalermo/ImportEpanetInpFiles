#(C)Marios Kyriakou 2016
#University of Cyprus, KIOS Research Center for Intelligent Systems and Networks
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QVariant, Qt

import os
from .Epa2GIS import epa2gis

# Initialize Qt resources from file resources.py, don't delete even if it
# shows not used
from . import resources_rc

class ImpEpanet(object):
  def __init__(self, iface):
    # Save a reference to the QGIS iface
    self.iface = iface
    self.plugin_dir = os.path.dirname(__file__)

  def initGui(self):
    # Create action
    self.action = QAction(QIcon(":/plugins/ImportEpanetInpFiles/impepanet.png"),"Import Epanet Input File",self.iface.mainWindow())
    self.action.setWhatsThis("Import Epanet Input File")
    #QObject.connect(self.action,SIGNAL("triggered()"),self.run)
    self.action.triggered.connect(self.run)
 
    self.iface.addToolBarIcon(self.action)
    self.iface.addPluginToMenu("&ImportEpanetInpFiles",self.action)

  def unload(self):
    # Remove the plugin
    self.iface.removePluginMenu("&ImportEpanetInpFiles",self.action)
    self.iface.removeToolBarIcon(self.action)

  def run(self):
    filePath = QFileDialog.getOpenFileName(self.iface.mainWindow(),"Choose EPANET Input file" , os.getcwd(), "Epanet Inp File (*.inp)")
    if filePath[0] == "":
      return
    epa2gis(filePath[0], self.plugin_dir)

    self.iface.messageBar().clearWidgets()
    msgBox = QMessageBox()
    msgBox.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
    msgBox.setWindowTitle('ImportEpanetInpFiles')
    msgBox.setText('Shapefiles have been created successfully in folder "_shapefiles_".')
    msgBox.exec_()