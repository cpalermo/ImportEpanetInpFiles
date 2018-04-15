# (C)Marios Kyriakou 2016
# University of Cyprus, KIOS Research Center for Intelligent Systems and Networks
import os
from Epa2GIS import epa2gis
from PyQt4.QtCore import QObject, SIGNAL, Qt
from PyQt4.QtGui import QAction, QIcon, QFileDialog, QMessageBox, QWidget
from .ExportEpanetInpFiles_dialog import ExportEpanetInpFilesDialog
import resources_rc


class ImpEpanet(object):
    def __init__(self, iface):
        # Save a reference to the QGIS iface
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.dlg = ExportEpanetInpFilesDialog()
        self.sections = ['junctions', 'tanks', 'pipes', 'pumps', 'reservoirs', 'valves', 'STATUS', 'PATTERNS', 'CURVES',
                         'CONTROLS', 'RULES', 'ENERGY', 'REACTIONS', 'REACTIONS_I', 'EMITTERS', 'QUALITY', 'SOURCES',
                         'MIXING', 'TIMES', 'REPORT', 'OPTIONS']

    def initGui(self):
        # Create action

        self.action = QAction(QIcon(":/plugins/ImportEpanetInpFiles/impepanet.png"), "Import Epanet Input File",
                              self.iface.mainWindow())
        self.action.setWhatsThis("Import Epanet Input File")
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&ImportEpanetInpFiles", self.action)

        self.actionexp = QAction(QIcon(":/plugins/ImportEpanetInpFiles/expepanet.png"), "Export Epanet Input File",
                                 self.iface.mainWindow())
        self.actionexp.setWhatsThis("Export Epanet Input File")
        QObject.connect(self.actionexp, SIGNAL("triggered()"), self.runexp)
        self.iface.addToolBarIcon(self.actionexp)
        self.iface.addPluginToMenu("&ImportEpanetInpFiles", self.actionexp)

        self.dlg.ok_button.clicked.connect(self.ok)
        self.dlg.cancel_button.clicked.connect(self.cancel)
        self.dlg.toolButtonOut.clicked.connect(self.toolButtonOut)

    def unload(self):
        # Remove the plugin
        self.iface.removePluginMenu("&ImportEpanetInpFiles", self.action)
        self.iface.removeToolBarIcon(self.action)

        self.iface.removePluginMenu("&ImportEpanetInpFiles", self.actionexp)
        self.iface.removeToolBarIcon(self.actionexp)

    def run(self):
        filePath = QFileDialog.getOpenFileName(self.iface.mainWindow(), "Choose EPANET Input file",
                                               os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop'),
                                               "Epanet Inp File (*.inp)")
        if filePath == "":
            return
        epa2gis(filePath)
        self.iface.messageBar().clearWidgets()
        msgBox = QMessageBox()
        msgBox.setWindowTitle('ImportEpanetInpFiles')
        msgBox.setText('Shapefiles have been created successfully in folder "_shapefiles_".')
        msgBox.exec_()

    def runexp(self):
        self.dlg.out.setText('')
        self.layers = self.canvas.layers()
        self.layer_list = []
        self.layer_list = ['NONE']
        [self.layer_list.append(layer.name()) for layer in self.layers]

        for sect in self.sections:
            eval('self.dlg.sect_' + sect + '.clear()')
            eval('self.dlg.sect_' + sect + '.addItems(self.layer_list)')
            indices = [i for i, s in enumerate(self.layer_list) if sect in s]
            if indices:
                if sect == 'REACTIONS':
                    eval('self.dlg.sect_' + sect + '.setCurrentIndex(indices[1])')
                else:
                    eval('self.dlg.sect_' + sect + '.setCurrentIndex(indices[0])')

        self.dlg.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.dlg.show()

    def cancel(self):
        self.dlg.close()
        self.layer_list = []
        self.layer_list = ['NONE']
        [eval('self.dlg.sect_' + sect + '.clear()') for sect in self.sections]

    def toolButtonOut(self):
        self.outEpanetName = QFileDialog.getSaveFileName(None, 'Save File',
                                                         os.path.join(os.path.join(os.path.expanduser('~')),
                                                                      'Desktop'), 'Epanet Inp File (*.inp)')
        self.dlg.out.setText(self.outEpanetName)

    def selectOutp(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle('Warning')
        msgBox.setText('Please define Epanet Inp File location.')
        msgBox.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        msgBox.exec_()
        return True

    def ok(self):
        # Here check if select OK button, get the layer fields
        # Initialize
        # [JUNCTIONS]
        if self.dlg.out.text() == '':
            if self.selectOutp():
                return
        elif os.path.isabs(self.dlg.out.text()) == False:
            if self.selectOutp():
                return

        self.outEpanetName = self.dlg.out.text()

        try:
            f = open(self.outEpanetName, "w")
            f.close()
        except:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Warning')
            msgBox.setText('Please define Epanet Inp File location.')
            msgBox.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
            msgBox.exec_()
            return

        if not self.layers:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Warning')
            msgBox.setText('No layers selected.')
            msgBox.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
            msgBox.exec_()
            return
        xypipes_id = []
        xypipesvert = []
        for sect in self.sections:
            exec 'sect' + sect + '=[]' in globals(), locals()
            exec 'xy' + sect + '=[]' in globals(), locals()
            if eval('self.dlg.sect_' + sect + '.currentText()') != 'NONE':
                # Get layer field names
                indLayerName = self.layer_list.index(eval('self.dlg.sect_' + sect + '.currentText()')) - 1
                fields = self.layers[indLayerName].pendingFields()
                field_names = [field.name() for field in fields]
                for elem in self.layers[indLayerName].getFeatures():
                    eval('sect' + sect + '.append(dict(zip(field_names, elem.attributes())))')
                    if any(sect in s for s in self.sections[0:5]):
                        geom = elem.geometry()
                        if self.layers[indLayerName].geometryType() == 0:
                            eval('xy' + sect + '.append(geom.asPoint())')
                        elif self.layers[indLayerName].geometryType() == 1:
                            eval('xy' + sect + '.append(geom.asPolyline())')
                            if sect == 'pipes':
                                if geom.asPolyline() > 2:
                                    for pp in range(len(geom.asPolyline())-2):
                                        xypipes_id.append(elem.attributes()[0])
                                        xypipesvert.append(geom.asPolyline()[pp])
                    if sect == 'junctions':
                        if 'Elevation' not in sectjunctions[0].keys():
                            QMessageBox.warning(QWidget(), "Message", "Elevation field is missing.")
        # (myDirectory,nameFile) = os.path.split(self.iface.activeLayer().dataProvider().dataSourceUri())
        my_directory = ''
        f = open(self.outEpanetName, 'wt')
        f.write('[TITLE]\n')
        f.write('Export input file via plugin ExportEpanetInpFiles. \n\n')
        f.write('[JUNCTIONS]\n')
        node_i_ds = []
        for i in range(len(sectjunctions)):
            node_i_ds.append(sectjunctions[i]['ID'])
            f.write(sectjunctions[i]['ID'] + '   ' + str(sectjunctions[i]['Elevation']) + '\n')
        f.write('\n[RESERVOIRS]\n')
        for i in range(len(sectreservoirs)):
            node_i_ds.append(sectreservoirs[i]['ID'])
            f.write(sectreservoirs[i]['ID'] + '   ' + str(sectreservoirs[i]['Head']) + '\n')
        f.write('\n[TANKS]\n')
        for i in range(len(secttanks)):
            node_i_ds.append(secttanks[i]['ID'])
            if secttanks[i]['VolumeCurv'] == None:
                secttanks[i]['VolumeCurv'] = ""
            f.write(secttanks[i]['ID'] + '   ' + str(secttanks[i]['Elevation']) + '   ' + str(secttanks[i]['InitLevel'])
                    + '   ' + str(secttanks[i]['MinLevel']) + '   ' + str(secttanks[i]['MaxLevel']) + '   ' + str(
                secttanks[i]['Diameter'])
                    + '   ' + str(secttanks[i]['MinVolume']) + '   ' + str(secttanks[i]['VolumeCurv']) + '   ' + '\n')
        f.write('\n[PIPES]\n')
        for i in range(len(sectpipes)):
            if (sectpipes[i]['NodeFrom'] in node_i_ds) and (sectpipes[i]['NodeTo'] in node_i_ds):
                f.write(sectpipes[i]['ID'] + '   ' + sectpipes[i]['NodeFrom']
                        + '   ' + sectpipes[i]['NodeTo'] + '   ' + str(sectpipes[i]['Length']) + '   ' + str(
                    sectpipes[i]['Diameter'])
                        + '   ' + str(sectpipes[i]['Roughness']) + '   ' + str(sectpipes[i]['MinorLoss']) + '   ' +
                        sectpipes[i]['Status'] + '\n')
        f.write('\n[PUMPS]\n')
        for i in range(len(sectpumps)):
            if sectpumps[i]['Curve'] != 'NULL':
                try:
                    sectpumps[i]['Curve'] = 'HEAD ' + sectpumps[i]['Curve']
                except:
                    sectpumps[i]['Curve'] = 'HEAD '
            else:
                sectpumps[i]['Curve'] = ''
            if sectpumps[i]['Pattern'] != 'NULL':
                try:
                    sectpumps[i]['Pattern'] = 'PATTERN ' + sectpumps[i]['Pattern']
                except:
                    sectpumps[i]['Pattern'] = "PATTERN "
            else:
                sectpumps[i]['Pattern'] = ''
            if sectpumps[i]['Power'] != 'NULL':
                try:
                    sectpumps[i]['Power'] = 'POWER ' + sectpumps[i]['Power']
                except:
                    sectpumps[i]['Power'] = "POWER "
            else:
                sectpumps[i]['Power'] = ''

            try:
                f.write(sectpumps[i]['ID'] + '   ' + sectpumps[i]['NodeFrom']
                        + '   ' + sectpumps[i]['NodeTo'] + '   ' + sectpumps[i]['Curve']
                        + '   ' + str(sectpumps[i]['Pattern']) + '   ' + str(sectpumps[i]['Power']) + '\n')
            except:
                f.write(sectpumps[i]['ID']  +'\n')

        f.write('\n[VALVES]\n')
        if self.dlg.sect_valves.currentText() != 'NONE':
            for i in range(len(sectvalves)):
                try:
                    sectvalves[i]['NodeFrom'] = sectvalves[i]['NodeFrom'] + ''
                except:
                    sectvalves[i]['NodeFrom'] = ""

                try:
                    sectvalves[i]['NodeTo'] = sectvalves[i]['NodeTo'] + ''
                except:
                    sectvalves[i]['NodeTo'] = ""
                f.write("{}   {}   {}   {}    {}    {}    {}\n".format(sectvalves[i]['ID'], sectvalves[i]['NodeFrom'],
                                                                       sectvalves[i]['NodeTo'],
                                                                       str(sectvalves[i]['Diameter']),
                                                                       sectvalves[i]['Type'],
                                                                       str(sectvalves[i]['Setting']),
                                                                       str(sectvalves[i]['MinorLoss'])))

        f.write('\n[DEMANDS]\n')
        for i in range(len(sectjunctions)):
            for u in range((len(sectjunctions[i]) - 2) / 2):
                if sectjunctions[i]['Demand' + str(u + 1)] == 0 and str(
                        sectjunctions[i]['Pattern' + str(u + 1)]) == 'None':
                    continue
                if str(sectjunctions[i]['Pattern' + str(u + 1)]) == 'NULL' or str(
                        sectjunctions[i]['Pattern' + str(u + 1)]) == 'None':
                    sectjunctions[i]['Pattern' + str(u + 1)] = ''
                f.write(sectjunctions[i]['ID'] + '   ' + str(sectjunctions[i]['Demand' + str(u + 1)])
                        + '   ' + str(sectjunctions[i]['Pattern' + str(u + 1)]) + '\n')

        f.write('\n[STATUS]\n')
        for i in range(len(sectSTATUS)):
            f.write("{}   {}\n".format(sectSTATUS[i]['Link_ID'], sectSTATUS[i]['Status/Set']))

        f.write('\n[PATTERNS]\n')
        for i in range(len(sectPATTERNS)):
            f.write("{}   {}\n".format(sectPATTERNS[i]['Pattern_ID'], sectPATTERNS[i]['Multiplier']))

        f.write('\n[CURVES]\n')
        for i in range(len(sectCURVES)):
            f.write(";{}:\n   {}   {}   {}\n".format(sectCURVES[i]['Type'], sectCURVES[i]['Curve_ID'],
                                                     str(sectCURVES[i]['X-Value']),str(sectCURVES[i]['Y-Value'])))

        f.write('\n[CONTROLS]\n')
        for i in range(len(sectCONTROLS)):
            f.write("{}\n".format(sectCONTROLS[i]['Controls']))

        f.write('\n[RULES]\n')
        for i in range(len(sectRULES)):
            f.write("RULE {}\n   {}\n".format(sectRULES[i]['Rule_ID'], sectRULES[i]['Rule']))

        f.write('\n[ENERGY]\n')
        if sectENERGY:
            try: f.write('Global Efficiency   ' + str(sectENERGY[0]['GlobalEffi']) + '\n')
            except: pass
            try: f.write('Global Price    ' + str(sectENERGY[0]['GlobalPric']) + '\n')
            except: pass
            try: f.write('Demand Charge   ' + str(sectENERGY[0]['DemCharge']) + '\n')
            except: pass

        f.write('\n[REACTIONS]\n')
        if sectREACTIONS:
            try: f.write('Order Bulk   ' + str(sectREACTIONS[0]['OrderBulk']) + '\n')
            except: pass
            try: f.write('Order Tank    ' + str(sectREACTIONS[0]['OrderTank']) + '\n')
            except: pass
            try: f.write('Order Wall   ' + str(sectREACTIONS[0]['OrderWall']) + '\n')
            except: pass
            try: f.write('Global Bulk   ' + str(sectREACTIONS[0]['GlobalBulk']) + '\n')
            except: pass
            try: f.write('Global Wall   ' + str(sectREACTIONS[0]['GlobalWall']) + '\n')
            except: pass
            try: f.write('Limiting Potential   ' + str(sectREACTIONS[0]['LimPotent']) + '\n')
            except: pass
            try: f.write('Roughness Correlation   ' + str(sectREACTIONS[0]['RoughCorr']) + '\n')
            except: pass

        f.write('\n[REACTIONS]\n')
        for i in range(len(sectREACTIONS_I)):
            f.write('{}    {}    {} \n'.format(sectREACTIONS_I[i]['Type'],
                                               sectREACTIONS_I[i]['Pipe/Tank'], str(sectREACTIONS_I[i]['Coeff.'])))
        f.write('\n[EMITTERS]\n')
        for i in range(len(sectEMITTERS)):
            f.write('{}    {}\n'.format(sectEMITTERS[i]['Junc_ID'], str(sectEMITTERS[i]['Coeff.'])))

        f.write('\n[SOURCES]\n')
        for i in range(len(sectSOURCES)):
            try:
                sectSOURCES[i]['Pattern'] = sectSOURCES[i]['Pattern']  + ''
            except:
                sectSOURCES[i]['Pattern'] = ''
            f.write("{}   {}   {}   {}\n".format(sectSOURCES[i]['Node_ID'], sectSOURCES[i]['Type'],
                                                                   str(sectSOURCES[i]['Strength']),
                                                                   sectSOURCES[i]['Pattern']))

        f.write('\n[MIXING]\n')
        for i in range(len(sectMIXING)):
            f.write('{}    {}    {} \n'.format(sectMIXING[i]['Tank_ID'],
                                               sectMIXING[i]['Model'], str(sectMIXING[i]['Fraction'])))

        f.write('\n[TIMES]\n')
        if sectTIMES:
            try: f.write('Duration   ' + str(sectTIMES[0]['Duration']) + '\n')
            except: pass
            try: f.write('Hydraulic Timestep    ' + str(sectTIMES[0]['HydStep']) + '\n')
            except: pass
            try: f.write('Quality Timestep   ' + str(sectTIMES[0]['QualStep']) + '\n')
            except: pass
            try: f.write('Pattern Timestep   ' + str(sectTIMES[0]['PatStep']) + '\n')
            except: pass
            try: f.write('Pattern Start   ' + str(sectTIMES[0]['PatStart']) + '\n')
            except: pass
            try: f.write('Report Timestep   ' + str(sectTIMES[0]['RepStep']) + '\n')
            except: pass
            try: f.write('Report Start   ' + str(sectTIMES[0]['RepStart']) + '\n')
            except: pass
            try: f.write('Start ClockTime   ' + str(sectTIMES[0]['StartClock']) + '\n')
            except: pass
            try: f.write('Statistic   ' + str(sectTIMES[0]['Statistic']) + '\n')
            except: pass

        f.write('\n[REPORT]\n')
        if sectREPORT:
            try: f.write('Status   ' + sectREPORT[0]['Status'] + '\n')
            except: pass
            try: f.write('Summary    ' + sectREPORT[0]['Summary'] + '\n')
            except: pass
            try: f.write('Page   ' + sectREPORT[0]['Page'] + '\n')
            except: pass

        f.write('\n[OPTIONS]\n')
        if sectOPTIONS:
            try: f.write('Units   ' + str(sectOPTIONS[0]['Units']) + '\n');
            except: pass
            try: f.write('Headloss    ' + str(sectOPTIONS[0]['Headloss']) + '\n')
            except: pass
            try: f.write('Specific Gravity   ' + str(sectOPTIONS[0]['SpecGrav']) + '\n')
            except: pass
            try: f.write('Viscosity   ' + str(sectOPTIONS[0]['Viscosity']) + '\n')
            except: pass
            try: f.write('Trials   ' + str(sectOPTIONS[0]['Trials']) + '\n')
            except: pass
            try: f.write('Accuracy   ' + str(sectOPTIONS[0]['Accuracy']) + '\n')
            except: pass
            try: f.write('CHECKFREQ   ' + str(sectOPTIONS[0]['CheckFreq']) + '\n')
            except: pass
            try: f.write('MAXCHECK   ' + str(sectOPTIONS[0]['MaxCheck']) + '\n')
            except: pass
            try: f.write('DAMPLIMIT   ' + str(sectOPTIONS[0]['DampLimit']) + '\n')
            except: pass
            try: f.write('Unbalanced   ' + str(sectOPTIONS[0]['Unbalanced']) + '\n')
            except: pass
            try: f.write('Pattern   ' + str(sectOPTIONS[0]['PatID']) + '\n')
            except: pass
            try: f.write('Demand Multiplier   ' + str(sectOPTIONS[0]['DemMult']) + '\n')
            except: pass
            try: f.write('Emitter Exponent   ' + str(sectOPTIONS[0]['EmitExp']) + '\n')
            except: pass
            try: f.write('Quality   ' + str(sectOPTIONS[0]['Quality']) + '\n')
            except: pass
            try: f.write('Diffusivity   ' + str(sectOPTIONS[0]['Diffusivit']) + '\n')
            except: pass
            try: f.write('Tolerance   ' + str(sectOPTIONS[0]['Tolerance']) + '\n')
            except: pass

        f.write('\n[COORDINATES]\n')
        for i in range(len(sectjunctions)):
            f.write(sectjunctions[i]['ID'] + '   ' + str(xyjunctions[i][0]) + '   ' + str(xyjunctions[i][1]) + '\n')
        for i in range(len(sectreservoirs)):
            f.write(sectreservoirs[i]['ID'] + '   ' + str(xyreservoirs[i][0]) + '   ' + str(xyreservoirs[i][1]) + '\n')
        for i in range(len(secttanks)):
            f.write(secttanks[i]['ID'] + '   ' + str(xytanks[i][0]) + '   ' + str(xytanks[i][1]) + '\n')

        f.write('\n[VERTICES]\n')

        for l in range(len(xypipes_id)):
                f.write(xypipes_id[l] + '   ' + str(xypipesvert[l][0]) + '   ' + str(xypipesvert[l][1]) + '\n')

        f.write('\n[END]\n')

        f.close()

        self.cancel()
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Export Options')
        msgBox.setText('Export Epanet Inp File "' + self.outEpanetName + '" succesful.')
        msgBox.exec_()
