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
    idx = epa2gis(filePath)
    file_extension = os.path.dirname(filePath)
    res = file_extension + '/_shapefiles_/'
    inpname = os.path.basename(filePath)
    shpfiles = []
    for dirpath, subdirs, files in os.walk(res):
        for x in files:
            if x.endswith(".shp"):
                shpfiles.append(os.path.join(dirpath, x))
    inp = res + inpname
    iface=self.iface

    # get python path plugin
    #getPathPlugin = os.path.dirname(os.path.realpath(__file__))+"\\"
    try:
        l4=iface.addVectorLayer(shpfiles[shpfiles.index(inp[:len(inp)-4]+'_pipes.shp')], inpname[:len(inpname)-4]+"_pipes", "ogr")
        iface.legendInterface().moveLayer( l4, idx )
        #l4.loadNamedStyle(getPathPlugin+"pipes.qml")
    except:
        pass
    try:
        l2=iface.addVectorLayer(shpfiles[shpfiles.index(inp[:len(inp)-4]+'_reservoirs.shp')], inpname[:len(inpname)-4]+"_reservoirs", "ogr")
        iface.legendInterface().moveLayer( l2, idx )
        #l2.loadNamedStyle(getPathPlugin+"reservoirs.qml")
    except:
        pass
    try:
        l3=iface.addVectorLayer(shpfiles[shpfiles.index(inp[:len(inp)-4]+'_tanks.shp')], inpname[:len(inpname)-4]+"_tanks", "ogr")
        iface.legendInterface().moveLayer( l3, idx )
        #l3.loadNamedStyle(getPathPlugin+"tanks.qml")
    except:
        pass
    try:
        l5=iface.addVectorLayer(shpfiles[shpfiles.index(inp[:len(inp)-4]+'_pumps.shp')], inpname[:len(inpname)-4]+"_pumps", "ogr")
        iface.legendInterface().moveLayer( l5, idx )
        #l5.loadNamedStyle(getPathPlugin+"pumps.qml")
    except:
        pass
    try:
        l6=iface.addVectorLayer(shpfiles[shpfiles.index(inp[:len(inp)-4]+'_valves.shp')], inpname[:len(inpname)-4]+"_valves", "ogr")
        iface.legendInterface().moveLayer( l6, idx )
        #l6.loadNamedStyle(getPathPlugin+"valves.qml")
    except:
        pass
    try:
        l1=iface.addVectorLayer(shpfiles[shpfiles.index(inp[:len(inp)-4]+'_junctions.shp')], inpname[:len(inpname)-4]+"_junctions", "ogr")
        iface.legendInterface().moveLayer( l1, idx )
        #l1.loadNamedStyle(getPathPlugin+"junctions.qml")
    except:
        pass
    #QgsMessageLog.logMessage("Shapefiles have been created successfully in folder _shapefiles_.")
    iface.messageBar().clearWidgets()
    msgBox = QMessageBox()
    msgBox.setWindowTitle('ImportEpanetInpFiles')
    msgBox.setText('Shapefiles have been created successfully in folder "_shapefiles_".')
    msgBox.exec_()