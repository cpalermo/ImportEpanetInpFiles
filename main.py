#(C)Marios Kyriakou 2016
#University of Cyprus, KIOS Research Center for Intelligent Systems and Networks
import qgis.utils, os
from Epa2Shp import epaShp
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
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
    epaShp(filePath)
    file_extension = os.path.dirname(filePath)
    res = file_extension + '/_shapefiles_/'
    inpname = os.path.basename(filePath)
    if inpname.index('.') != len(inpname)-4:
        qgis.utils.iface.messageBar().clearWidgets()
        msgBox = QMessageBox()
        msgBox.setWindowTitle('ImportEpanetInpFiles')
        msgBox.setText('Warning name of input file.')
        msgBox.exec_()
        return

    shpfiles = []
    for dirpath, subdirs, files in os.walk(res):
        for x in files:
            if x.endswith(".shp"):
                shpfiles.append(os.path.join(dirpath, x))
    inp = res + inpname
    a1=inp[:len(inp)-4]+'_junctions.shp'
    a2=inp[:len(inp)-4]+'_reservoirs.shp'
    a3=inp[:len(inp)-4]+'_tanks.shp'
    a4=inp[:len(inp)-4]+'_pipes.shp'
    a5=inp[:len(inp)-4]+'_pumps.shp'
    a6=inp[:len(inp)-4]+'_valves.shp'
    iface=qgis.utils.iface
    # get python path plugin
    #getPathPlugin = os.path.dirname(os.path.realpath(__file__))+"\\"
    for i in range(0,len(shpfiles)):
      if a1==shpfiles[i]:#junctions
          l1=iface.addVectorLayer(shpfiles[i], inpname[:len(inpname)-4]+"_junctions", "ogr")
          #l1.loadNamedStyle(getPathPlugin+"junctions.qml")
      if a2==shpfiles[i]:#reservoirs
          l2=iface.addVectorLayer(shpfiles[i], inpname[:len(inpname)-4]+"_reservoirs", "ogr")
          #l2.loadNamedStyle(getPathPlugin+"reservoirs.qml")
      if a3==shpfiles[i]:#tanks
          l3=iface.addVectorLayer(shpfiles[i], inpname[:len(inpname)-4]+"_tanks", "ogr")
          #l3.loadNamedStyle(getPathPlugin+"tanks.qml")
      if a4==shpfiles[i]:#pipes
          l3=iface.addVectorLayer(shpfiles[i], inpname[:len(inpname)-4]+"_pipes", "ogr")
          #l3.loadNamedStyle(getPathPlugin+"pipes.qml")
      if a5==shpfiles[i]:#pumps
          l4=iface.addVectorLayer(shpfiles[i], inpname[:len(inpname)-4]+"_pumps", "ogr")
          #l4.loadNamedStyle(getPathPlugin+"pumps.qml")
      if a6==shpfiles[i]:#valves
          l5=iface.addVectorLayer(shpfiles[i], inpname[:len(inpname)-4]+"_valves", "ogr")
          #l5.loadNamedStyle(getPathPlugin+"valves.qml")
      #iface.actionToggleEditing().trigger()
      #iface.actionToggleEditing().trigger()
    #clear warnings


    qgis.utils.iface.messageBar().clearWidgets()
    msgBox = QMessageBox()
    msgBox.setWindowTitle('ImportEpanetInpFiles')
    msgBox.setText('Shapefiles have been created successfully in folder "_shapefiles_".')
    msgBox.exec_()