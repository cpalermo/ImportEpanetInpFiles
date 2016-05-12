#(C)Marios Kyriakou 2016
#University of Cyprus, KIOS Research Center for Intelligent Systems and Networks
#import qgis.utils
import os
from Epa2GIS import epa2gis
from PyQt4.QtCore import QObject, SIGNAL
from PyQt4.QtGui import QAction, QIcon, QFileDialog, QMessageBox
import resources_rc

class ImpEpanet(object):
  def __init__(self, iface):
    # Save a reference to the QGIS iface
    self.iface = iface

  def initGui(self):
    # Create action
    self.action = QAction(QIcon(":/plugins/ImportEpanetInpFiles/impepanet.png"),"Import Epanet Input File",self.iface.mainWindow())
    self.action.setWhatsThis("Import Epanet Input File")
    QObject.connect(self.action,SIGNAL("triggered()"),self.run)
    self.iface.addToolBarIcon(self.action)
    self.iface.addPluginToMenu("&ImportEpanetInpFiles",self.action)

  def unload(self):
    # Remove the plugin
    self.iface.removePluginMenu("&ImportEpanetInpFiles",self.action)
    self.iface.removeToolBarIcon(self.action)

  def run(self):
    filePath = QFileDialog.getOpenFileName(self.iface.mainWindow(),"Choose EPANET Input file" , os.getcwd(), "Epanet Inp File (*.inp)")
    if filePath == "":
      return
    s = epa2gis(filePath)
    idx=s[0]
    pb=s[1]
    pb.setValue(100)
    self.iface.messageBar().clearWidgets()
    msgBox = QMessageBox()
    msgBox.setWindowTitle('ImportEpanetInpFiles')
    msgBox.setText('Shapefiles have been created successfully in folder "_shapefiles_".')
    msgBox.exec_()