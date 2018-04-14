#(C)Marios Kyriakou 2016
#University of Cyprus, KIOS Research Center for Intelligent Systems and Networks
import readEpanetFile as d
from qgis.core import QgsFeature,QgsVectorLayer,QgsVectorFileWriter,QgsField,QgsPoint,QgsGeometry
import qgis.utils, os
from PyQt4.QtGui import QProgressBar
from qgis.gui import QgsMessageBar
from PyQt4.QtCore import QVariant
import collections
import numpy as np

def epa2gis(inpname):
    file_extension = os.path.dirname(inpname)
    inpname = os.path.basename(inpname)
    inp = file_extension + '/'+ inpname
    if len(file_extension)==0:
        inp = inpname
    newpath = file_extension + '/_shapefiles_'
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    iface=qgis.utils.iface
    d.LoadFile(inp)
    d.BinUpdateClass()
    nlinkCount=d.getBinLinkCount()
    res = newpath + '\\'
    saveFile=res+inpname[:len(inpname)-4]

    #Get all Sections
    mixing = d.getMixingSection()
    reactions = d.getReactionsSection()
    sources = d.getSourcesSection()
    rules = d.getRulesSection()
    quality = d.getQualitySection()
    curves = d.getCurvesSection()
    patterns = d.getPatternsSection()
    controls = d.getControlsSection()
    emitters = d.getEmittersSection()
    status = d.getStatusSection()
    demands = d.getDemandsSection()
    energy = d.getEnergySection()
    optReactions = d.getReactionsOptionsSection()
    times = d.getTimesSection()
    report = d.getReportSection()
    options = d.getOptionsSection()

    #Get all Section lengths
    allSections=[len(energy),len(optReactions),len(demands),len(status),len(emitters),len(controls),len(patterns),
                 len(curves[0]),len(quality),len(rules),len(sources),len(reactions),len(mixing),len(times),len(report),
                 len(options),d.getBinNodeCount(),d.getBinLinkCount()]
    ss=max(allSections)
    idx = iface.legendInterface().addGroup(inpname[:len(inpname)-4])
    xy=d.getBinNodeCoordinates()
    x=xy[0]
    y=xy[1]
    vertx=xy[2]
    verty=xy[3]
    vertxyFinal=[]
    for i in range(len(vertx)):
        vertxy=[]
        for u in range(len(vertx[i])):
            vertxy.append([float(vertx[i][u]),float(verty[i][u])])
        if vertxy!=[]:
            vertxyFinal.append(vertxy)

    otherDemads = d.getBinNodeBaseDemandsDemSection()
    ndID = d.getBinNodeNameID()
    ndBaseD = d.getBinNodeBaseDemands()
    ndPatID = d.getBinNodeDemandPatternID()
    otherDemadsIndex = []
    otherDemadsPatterns = []
    for i, p in enumerate(otherDemads[1]):
        otherDemadsIndex.append(ndID.index(p))
        otherDemadsPatterns.append(otherDemads[2][i])
    counter = collections.Counter(otherDemadsIndex)
    maxCategories = 1
    if counter:
        maxCategories = max(counter.values())

    if not ndBaseD:
        ndBaseD = otherDemads[0]

    #Get data of Junctions
    if d.getBinNodeJunctionCount()>0:
        ndBaseTmp = np.empty((len(ndBaseD), maxCategories,))
        ndPatTmp = []
        for t in range(0,maxCategories):
            for u in range(0,len(ndBaseD)):
                ndBaseTmp[u][t] = 0
                ndPatTmp.append(['None']*2)

        for uu in range(0,len(ndBaseD)):
            if d.getBinNodeBaseDemands():
                ndBaseTmp[uu][0] = ndBaseD[uu]
                ndPatTmp[uu][0] = ndPatID[uu]
        t=0
        for i, p in enumerate(otherDemadsIndex):
            if d.getBinNodeBaseDemands():
                ndBaseTmp[p][t] = ndBaseD[otherDemadsIndex[i]]
                ndPatTmp[p][t] = ndPatID[otherDemadsIndex[i]]
            else:
                ndBaseTmp[p][t] = otherDemads[0][i]
                ndPatTmp[p][t] = otherDemads[2][i]

            t=t+1
            if t>max(counter.values())-1:
               t=max(counter.values())-1
            if i>0:
               if otherDemadsIndex[i-1]==p:
                  ndBaseTmp[p][t] = otherDemads[0][i]
                  ndPatTmp[p][t] = otherDemads[2][i]
                  t = t - 1
        # Write Junction Shapefile
        fields=["ID","Elevation"]#,"pattern","demand"]
        fieldsCode=[0,1]
        for u in range(0,maxCategories):
            fields.append('Demand' + str(u+1)); fields.append('Pattern' + str(u+1))
            fieldsCode.append(1); fieldsCode.append(0)
        posJunction = QgsVectorLayer("point", "Junctions", "memory")
        prJunction = posJunction.dataProvider()

        ndBaseTmp = ndBaseTmp.tolist()

        createColumnsAttrb(prJunction,fields,fieldsCode)
        posJunction.startEditing()
        ndEle=d.getBinNodeJunctionElevations()

    #Get data of Pipes
    #Write shapefile pipe
    if nlinkCount>0:
        posPipe = QgsVectorLayer("LineString", "Pipes", "memory")
        prPipe = posPipe.dataProvider()
        fields=["ID","NodeFrom","NodeTo","Status","Length","Diameter","Roughness","MinorLoss"]
        fieldsCode=[0,0,0,0,1,1,1,1]
        createColumnsAttrb(prPipe,fields,fieldsCode)
        posPipe.startEditing()

        pIndex = d.getBinLinkPumpIndex()
        vIndex = d.getBinLinkValveIndex()
        ndlConn=d.getBinNodesConnectingLinksID()
        x1=[];x2=[];y1=[];y2=[]
        stat=d.getBinLinkInitialStatus()

        kk=0; ch=0
        linkID=d.getBinLinkNameID()
        linkLengths=d.getBinLinkLength()
        linkDiameters=d.getBinLinkDiameter()
        linkRough=d.getBinLinkRoughnessCoeff()
        linkMinorloss=d.getBinLinkMinorLossCoeff()

    # Write Tank Shapefile and get tank data
    if d.getBinNodeTankCount()>0:
        posTank = QgsVectorLayer("point", "Reservoirs", "memory")
        prTank = posTank.dataProvider()
        fields=["ID","Elevation","InitLevel","MinLevel","MaxLevel","Diameter","MinVolume","VolumeCurve"]
        fieldsCode=[0,1,1,1,1,1,1,1]
        createColumnsAttrb(prTank,fields,fieldsCode)
        posTank.startEditing()

        ndTankelevation=d.getBinNodeTankElevations()
        initiallev=d.getBinNodeTankInitialLevel()
        minimumlev=d.getBinNodeTankMinimumWaterLevel()
        maximumlev=d.getBinNodeTankMaximumWaterLevel()
        diameter=d.getBinNodeTankDiameter()
        minimumvol=d.getBinNodeTankMinimumWaterVolume()
        volumecurv=d.getBinNodeTankVolumeCurveID()
        ndTankID=d.getBinNodeTankNameID()

    # Write Reservoir Shapefile
    if d.getBinNodeReservoirCount()>0:
        posReservoirs = QgsVectorLayer("point", "Reservoirs", "memory")
        prReservoirs = posReservoirs.dataProvider()
        fields=["ID","Head"]
        fieldsCode=[0,1]
        createColumnsAttrb(prReservoirs,fields,fieldsCode)
        head=d.getBinNodeReservoirElevations()
        posReservoirs.startEditing()
    if times!=[]:
        posTimes = QgsVectorLayer("point", "Times", "memory")
        prTimes = posTimes.dataProvider()
    if energy!=[]:
        posE = QgsVectorLayer("point", "Energy", "memory")
        prE = posE.dataProvider()
    if report!=[]:
        posRep = QgsVectorLayer("point", "Report", "memory")
        prRep = posRep.dataProvider()
    if options!=[]:
        posOpt = QgsVectorLayer("point", "Options", "memory")
        prOpt = posOpt.dataProvider()
    if optReactions!=[]:
        posO = QgsVectorLayer("point", "Reactions", "memory")
        prO = posO.dataProvider()

    ppE=[];ppO=[];ppTimes=[];ppRep=[];ppOpt=[]
    ppMix=[];ppReactions=[];ppSourc=[];ppRul=[];ppPat=[]
    ppQual=[];ppDem=[];ppStat=[];ppEmit=[];ppCont=[];ppCurv=[]
    vvLink=68

    for i in range(ss):
        if i==ss/vvLink and vvLink>-1:
            vvLink=vvLink-1

        if i<d.getBinNodeJunctionCount():
            featJ = QgsFeature()
            point = QgsPoint(float(x[i]), float(y[i]))
            featJ.initAttributes(2+len(ndBaseTmp[0])*2)
            featJ.setGeometry(QgsGeometry.fromPoint(point))
            featJ.setAttribute(0, ndID[i])
            featJ.setAttribute(1, ndEle[i])
            w=2
            for j in range(0, len(ndBaseTmp[0])):
                featJ.setAttribute(w, ndBaseTmp[i][j])
                featJ.setAttribute(w+1, ndPatTmp[i][j])
                w=w+2
            prJunction.addFeatures([featJ])

        if i<nlinkCount:
                if len(stat)==i:
                    ch=1
                if ch==1:
                    stat.append('OPEN')

                x1.append(x[ndID.index(d.getBinLinkFromNode()[i])])
                y1.append(y[ndID.index(d.getBinLinkFromNode()[i])])
                x2.append(x[ndID.index(d.getBinLinkToNode()[i])])
                y2.append(y[ndID.index(d.getBinLinkToNode()[i])])

                if i in pIndex:
                    xx= (float(x1[i])+float(x2[i]))/2
                    yy= (float(y1[i])+float(y2[i]))/2
                    for p in range(0,2):
                        if p==0:
                            linkIDFinal=linkID[i]+'_pump1'
                            node1=ndlConn[0][i]
                            node2=linkIDFinal
                            indN1 = d.getBinNodeIndex(node1)
                            point1 = QgsPoint(float(x[indN1]),float(y[indN1]))
                            point2 = QgsPoint(xx,yy)
                        elif p==1:
                            linkIDFinal=linkID[i]+'_pump2'
                            node1=linkIDFinal
                            node2=ndlConn[1][i]
                            indN2 = d.getBinNodeIndex(node2)
                            point2 = QgsPoint(float(x[indN2]),float(y[indN2]))
                            point1 = QgsPoint(xx,yy)
                        length=0
                        diameter=0
                        roughness=0
                        minorloss=0

                        featPipe = QgsFeature()
                        featPipe.setGeometry((QgsGeometry.fromPolyline([point1,point2])))
                        featPipe.setAttributes([linkIDFinal,node1,node2,stat[i],length,diameter,roughness,minorloss])
                        prPipe.addFeatures([featPipe])

                elif i in vIndex:
                    xx= (float(x1[i])+float(x2[i]))/2
                    yy= (float(y1[i])+float(y2[i]))/2
                    for v in range(0,2):
                        if v==0:
                            linkIDFinal=linkID[i]+'_valve1'
                            node1=ndlConn[0][i]
                            node2=linkIDFinal
                            indN1 = d.getBinNodeIndex(node1)
                            point1 = QgsPoint(float(x[indN1]),float(y[indN1]))
                            point2 = QgsPoint(xx,yy)
                        elif v==1:
                            linkIDFinal=linkID[i]+'_valve2'
                            node1=linkIDFinal
                            node2=ndlConn[1][i]
                            indN2 = d.getBinNodeIndex(node2)

                            point2 = QgsPoint(float(x[indN2]),float(y[indN2]))
                            point1 = QgsPoint(xx,yy)

                        length=0
                        diameter=0
                        roughness=0
                        minorloss=0

                        featPipe = QgsFeature()
                        featPipe.setGeometry((QgsGeometry.fromPolyline([point1,point2])))
                        featPipe.setAttributes([linkIDFinal,node1,node2,stat[i],length,diameter,roughness,minorloss])
                        prPipe.addFeatures([featPipe])
                else:
                    point1 = QgsPoint(float(x1[i]),float(y1[i]))
                    point2 = QgsPoint(float(x2[i]),float(y2[i]))
                    if vertx[i]!=[]:
                        parts=[]
                        parts.append(point1)
                        for mm in range(len(vertxyFinal[kk])):
                            a=vertxyFinal[kk][mm]
                            parts.append(QgsPoint(a[0],a[1]))
                        parts.append(point2)
                        featPipe = QgsFeature()
                        featPipe.setGeometry((QgsGeometry.fromPolyline(parts)))
                        kk=kk+1
                    else:
                        featPipe = QgsFeature()
                        point1 = QgsPoint(float(x1[i]),float(y1[i]))
                        point2 = QgsPoint(float(x2[i]),float(y2[i]))
                        featPipe.setGeometry(QgsGeometry.fromPolyline([point1,point2]))

                    featPipe.setAttributes([linkID[i],ndlConn[0][i],ndlConn[1][i],stat[i],linkLengths[i],linkDiameters[i],linkRough[i],linkMinorloss[i]])
                    prPipe.addFeatures([featPipe])

        if i<d.getBinNodeTankCount():
            p=d.getBinNodeTankIndex()[i]-1
            featTank = QgsFeature()
            point = QgsPoint(float(x[p]), float(y[p]))
            featTank.setGeometry(QgsGeometry.fromPoint(point))
            featTank.setAttributes([ndTankID[i],ndTankelevation[i],initiallev[i],minimumlev[i],maximumlev[i],diameter[i],minimumvol[i],volumecurv[i]])
            prTank.addFeatures([featTank])

        if i<d.getBinNodeReservoirCount():
            p=d.getBinNodeReservoirIndex()[i]-1
            feature = QgsFeature()
            point = QgsPoint(float(x[p]), float(y[p]))
            feature.setGeometry(QgsGeometry.fromPoint(point))
            feature.setAttributes([ndID[p],head[i]])
            prReservoirs.addFeatures([feature])

        if i<allSections[12]:
            if len(mixing[i])==3:
                ppMix.append([mixing[i][0],mixing[i][1],mixing[i][2]])
            else:
                ppMix.append([mixing[i][0],mixing[i][1]])
        if i<allSections[11]:
            ppReactions.append([reactions[i][0],reactions[i][1],reactions[i][2]])
        if i<allSections[10]:
            ppSourc.append([sources[i][0],sources[i][1]])
            if len(sources[i])>2:
                ppSourc.append([sources[i][0],sources[i][1],sources[i][2]])
        if i<allSections[9]:
            if len(rules[i])>2:
                ppRul.append([rules[i][0][1][1],rules[i][1][0]+rules[i][2][0]+rules[i][3][0]])
        if i<allSections[8]:
            ppQual.append([quality[i][0],quality[i][1]])
        if i<allSections[7]:
            ppCurv.append([str(curves[0][i][0]),str(curves[0][i][1]),str(curves[0][i][2]),str(curves[1][i])])
        if i<allSections[6]:
            ppPat.append([patterns[i][0],str(patterns[i][1])])
        if i<allSections[5]:
            ppCont.append([controls[i]])
        if i<allSections[4]:
            ppEmit.append([emitters[i][0],emitters[i][1]])
        if i<allSections[3]:
            ppStat.append([status[i][0],status[i][1]])
        if i<allSections[2]:
            if len(demands[i])>2:
                ppDem.append([demands[i][0],demands[i][1],demands[i][2]])
        if i<allSections[0]:
            mm = energy[i][0]
            if mm.upper()=="GLOBAL":
                prE.addAttributes( [ QgsField("Global"+energy[i][1], QVariant.String) ] )
                if len(energy[i])>2:
                    ppE.append(energy[i][2])
                else:
                    ppE.append('')
            if mm.upper()=="PUMP":
                prE.addAttributes( [ QgsField("Pump", QVariant.String) ] )
                if len(energy[i])>2:
                    ppE.append(energy[i][1]+' '+energy[i][2])
                else:
                    ppE.append(energy[i][1])
            elif mm.upper()=="DEMAND":
                if energy[i][1].upper()=="CHARGE":
                    prE.addAttributes( [ QgsField("DemCharge", QVariant.String) ] )
                    if len(energy[i])>2:
                        ppE.append(energy[i][2])
        if i<allSections[1]:
            mm = optReactions[i][0]
            if mm.upper()=="ORDER":
                prO.addAttributes( [ QgsField("Order"+optReactions[i][1], QVariant.String) ] )
                if len(optReactions[i])>2:
                    ppO.append(optReactions[i][2])
                else:
                    ppO.append('')
            elif mm.upper()=="GLOBAL":
                prO.addAttributes( [ QgsField("Global"+optReactions[i][1], QVariant.String) ] )
                if len(optReactions[i])>2:
                    ppO.append(optReactions[i][2])
                else:
                    ppO.append('')
            elif mm.upper()=="BULK":
                prO.addAttributes( [ QgsField("Bulk", QVariant.String) ] )
                if len(optReactions[i])>2:
                    ppO.append(optReactions[i][1]+' '+optReactions[i][2])
                else:
                    ppO.append(optReactions[i][1])
            elif mm.upper()=="WALL":
                prO.addAttributes( [ QgsField("Wall", QVariant.String) ] )
                if len(optReactions[i])>2:
                    ppO.append(optReactions[i][1]+' '+optReactions[i][2])
                else:
                    ppO.append(optReactions[i][1])
            elif mm.upper()=="TANK":
                prO.addAttributes( [ QgsField("Tank", QVariant.String) ] )
                if len(optReactions[i])>2:
                    ppO.append(optReactions[i][1]+' '+optReactions[i][2])
                else:
                    ppO.append(optReactions[i][1])
            elif mm.upper()=="LIMITING":
                if optReactions[i][1].upper()=="POTENTIAL":
                    prO.addAttributes( [ QgsField("LimPotent", QVariant.String) ] )
                    if len(optReactions[i])>2:
                        ppO.append(optReactions[i][2])
            elif mm.upper()=="ROUGHNESS":
                if optReactions[i][1].upper()=="CORRELATION":
                    prO.addAttributes( [ QgsField("RoughCorr", QVariant.String) ] )
                    if len(optReactions[i])>2:
                        ppO.append(optReactions[i][2])
        if i<allSections[13]:
            mm = times[i][0]
            if mm.upper()=="DURATION":
                prTimes.addAttributes( [ QgsField("Duration", QVariant.String) ] )
                ppTimes.append(times[i][1])
            if mm.upper()=="HYDRAULIC":
                prTimes.addAttributes( [ QgsField("HydStep", QVariant.String) ] )
                ppTimes.append(times[i][2])
            elif mm.upper()=="QUALITY":
                prTimes.addAttributes( [ QgsField("QualStep", QVariant.String) ] )
                ppTimes.append(times[i][2])
            elif mm.upper()=="RULE":
                prTimes.addAttributes( [ QgsField("RuleStep", QVariant.String) ] )
                ppTimes.append(times[i][2])
            elif mm.upper()=="PATTERN":
                if times[i][1].upper()=="TIMESTEP":
                    prTimes.addAttributes( [ QgsField("PatStep", QVariant.String) ] )
                    ppTimes.append(times[i][2])
                if times[i][1].upper()=="START":
                    prTimes.addAttributes( [ QgsField("PatStart", QVariant.String) ] )
                    ppTimes.append(times[i][2])
            elif mm.upper()=="REPORT":
                if times[i][1].upper()=="TIMESTEP":
                    prTimes.addAttributes( [ QgsField("RepStep", QVariant.String) ] )
                    ppTimes.append(times[i][2])
                if times[i][1].upper()=="START":
                    prTimes.addAttributes( [ QgsField("RepStart", QVariant.String) ] )
                    ppTimes.append(times[i][2])
            elif mm.upper()=="START":
                if times[i][1].upper()=="CLOCKTIME":
                    prTimes.addAttributes( [ QgsField("StartClock", QVariant.String) ] )
                    if len(times[i])>3:
                        ppTimes.append(times[i][2]+' '+times[i][3])
                    else:
                        ppTimes.append(times[i][2])
            elif mm.upper()=="STATISTIC":
                prTimes.addAttributes( [ QgsField("Statistic", QVariant.String) ] )
                if times[i][1].upper()=='NONE' or times[i][1].upper()=='AVERAGE' or times[i][1].upper()=='MINIMUM' or times[i][1].upper()=='MAXIMUM' or times[i][1].upper()=='RANGE':
                    ppTimes.append(times[i][1])
        if i<allSections[14]:
            mm = report[i][0]
            if mm.upper()=="PAGESIZE":
                prRep.addAttributes( [ QgsField("PageSize", QVariant.String) ] )
                ppRep.append(report[i][1])
            if mm.upper()=="FILE":
                prRep.addAttributes( [ QgsField("FileName", QVariant.String) ] )
                ppRep.append(report[i][1])
            elif mm.upper()=="STATUS":
                prRep.addAttributes( [ QgsField("Status", QVariant.String) ] )
                ppRep.append(report[i][1])
            elif mm.upper()=="SUMMARY":
                prRep.addAttributes( [ QgsField("Summary", QVariant.String) ] )
                ppRep.append(report[i][1])
            elif mm.upper()=="ENERGY":
                prRep.addAttributes( [ QgsField("Energy", QVariant.String) ] )
                ppRep.append(report[i][1])
            elif mm.upper()=="NODES":
                prRep.addAttributes( [ QgsField("Nodes", QVariant.String) ] )
                if len(report[i])>2:
                    ppRep.append(report[i][1]+' '+report[i][2])
                else:
                    ppRep.append(report[i][1])
            elif mm.upper()=="LINKS":
                prRep.addAttributes( [ QgsField("Links", QVariant.String) ] )
                if len(report[i])>2:
                    ppRep.append(report[i][1]+' '+report[i][2])
                else:
                    ppRep.append(report[i][1])
            else:
                prRep.addAttributes( [ QgsField(mm, QVariant.String) ] )
                if len(report[i])>2:
                    ppRep.append(report[i][1]+' '+report[i][2])
                else:
                    ppRep.append(report[i][1])
        if i<allSections[15]:
            mm = options[i][0]
            if mm.upper()=="UNITS":
                prOpt.addAttributes( [ QgsField("Units", QVariant.String) ] )
                ppOpt.append(options[i][1])
            if mm.upper()=="HYDRAULICS":
                prOpt.addAttributes( [ QgsField("Hydraulics", QVariant.String) ] )
                if len(options[i])>2:
                    ppOpt.append(options[i][1]+' '+options[i][2])
                else:
                    ppOpt.append(options[i][1])
            elif mm.upper()=="QUALITY":
                prOpt.addAttributes( [ QgsField("Quality", QVariant.String) ] )
                if len(options[i])>2:
                    ppOpt.append(options[i][1]+' '+options[i][2])
                elif len(options[i])>3:
                    ppOpt.append(options[i][1]+' '+options[i][2]+' '+options[i][3])
                else:
                    ppOpt.append(options[i][1])
            elif mm.upper()=="VISCOSITY":
                prOpt.addAttributes( [ QgsField("Viscosity", QVariant.String) ] )
                ppOpt.append(options[i][1])
            elif mm.upper()=="DIFFUSIVITY":
                prOpt.addAttributes( [ QgsField("Diffusivity", QVariant.String) ] )
                ppOpt.append(options[i][1])
            elif mm.upper()=="SPECIFIC":
                if options[i][1].upper()=="GRAVITY":
                    prOpt.addAttributes( [ QgsField("SpecGrav", QVariant.String) ] )
                    ppOpt.append(options[i][2])
            elif mm.upper()=="TRIALS":
                prOpt.addAttributes( [ QgsField("Trials", QVariant.String) ] )
                ppOpt.append(options[i][1])
            elif mm.upper()=="HEADLOSS":
                prOpt.addAttributes( [ QgsField("Headloss", QVariant.String) ] )
                ppOpt.append(options[i][1])
            elif mm.upper()=="ACCURACY":
                prOpt.addAttributes( [ QgsField("Accuracy", QVariant.String) ] )
                ppOpt.append(options[i][1])
            elif mm.upper()=="UNBALANCED":
                prOpt.addAttributes( [ QgsField("Unbalanced", QVariant.String) ] )
                if len(options[i])>2:
                    ppOpt.append(options[i][1]+' '+options[i][2])
                else:
                    ppOpt.append(options[i][1])
            elif mm.upper()=="PATTERN":
                prOpt.addAttributes( [ QgsField("PatID", QVariant.String) ] )
                ppOpt.append(options[i][1])
            elif mm.upper()=="TOLERANCE":
                prOpt.addAttributes( [ QgsField("Tolerance", QVariant.String) ] )
                ppOpt.append(options[i][1])
            elif mm.upper()=="MAP":
                prOpt.addAttributes( [ QgsField("Map", QVariant.String) ] )
                ppOpt.append(options[i][1])
            elif mm.upper()=="DEMAND":
                if options[i][1].upper()=="MULTIPLIER":
                    prOpt.addAttributes( [ QgsField("DemMult", QVariant.String) ] )
                    ppOpt.append(options[i][2])
            elif mm.upper()=="EMITTER":
                if options[i][1].upper()=="EXPONENT":
                    prOpt.addAttributes( [ QgsField("EmitExp", QVariant.String) ] )
                    ppOpt.append(options[i][2])
            elif mm.upper()=="CHECKFREQ":
                prOpt.addAttributes( [ QgsField("CheckFreq", QVariant.String) ] )
                ppOpt.append(options[i][1])
            elif mm.upper()=="MAXCHECK":
                prOpt.addAttributes( [ QgsField("MaxCheck", QVariant.String) ] )
                ppOpt.append(options[i][1])
            elif mm.upper()=="DAMPLIMIT":
                prOpt.addAttributes( [ QgsField("DampLimit", QVariant.String) ] )
                ppOpt.append(options[i][1])

    if options!=[]:
        writeDBF(posOpt,[ppOpt],prOpt,saveFile,inpname, "_OPTIONS", iface,idx)

    if report!=[]:
        writeDBF(posRep,[ppRep],prRep,saveFile,inpname, "_REPORT", iface,idx)

    if times!=[]:
        writeDBF(posTimes,[ppTimes],prTimes,saveFile,inpname, "_TIMES", iface,idx)

    if energy!=[]:
        writeDBF(posE,[ppE],prE,saveFile,inpname, "_ENERGY", iface,idx)

    if optReactions!=[]:
        writeDBF(posO,[ppO],prO,saveFile,inpname, "_REACTIONS", iface,idx)

    if mixing!=[]:
        posMix = QgsVectorLayer("point", "Mixing", "memory")
        prMix = posMix.dataProvider()
        fields=["Tank_ID","Model","Fraction"]
        fieldsCode=[0,0,1] #0 String, 1 Double
        createColumnsAttrb(prMix,fields,fieldsCode)
        writeDBF(posMix,ppMix,prMix,saveFile,inpname, "_MIXING", iface,idx)

    if reactions!=[]:
        posReact = QgsVectorLayer("point", "ReactionsInfo", "memory")
        prReact = posReact.dataProvider()
        fields=["Type","Pipe/Tank","Coeff."]; fieldsCode=[0,0,1]
        createColumnsAttrb(prReact,fields,fieldsCode)
        writeDBF(posReact,ppReactions,prReact,saveFile,inpname, "_REACTIONSinfo", iface,idx)

    if sources!=[]:
        posSourc = QgsVectorLayer("point", "Sources", "memory")
        prSourc = posSourc.dataProvider()
        fields=["Node_ID","Type","Strength","Pattern"]; fieldsCode=[0,0,1,0]
        createColumnsAttrb(prSourc,fields,fieldsCode)
        writeDBF(posSourc,ppSourc,prSourc,saveFile,inpname, "_SOURCES", iface,idx)

    if rules!=[] and len(rules[0])>3:
        posRul = QgsVectorLayer("point", "Rules", "memory")
        prRul = posRul.dataProvider()
        fields=["Rule_ID","Rule"]; fieldsCode=[0,0]
        createColumnsAttrb(prRul,fields,fieldsCode)
        writeDBF(posRul,ppRul,prRul,saveFile,inpname, "_RULES", iface,idx)

    if ppQual!=[]:
        posQual = QgsVectorLayer("point", "Sources", "memory")
        prQual = posQual.dataProvider()
        fields=["Node_ID","Init_Qual"]; fieldsCode=[0,1]
        createColumnsAttrb(prQual,fields,fieldsCode)
        writeDBF(posQual,ppQual,prQual,saveFile,inpname, "_QUALITY", iface,idx)

    # if demands!=[]:
    #     posDem = QgsVectorLayer("point", "Demands", "memory")
    #     prDem = posDem.dataProvider()
    #     fields=["ID","Demand","Pattern"]; fieldsCode=[0,1,0]
    #     createColumnsAttrb(prDem,fields,fieldsCode)
    #     writeDBF(posDem,ppDem,prDem,saveFile,inpname, "_DEMANDS", iface,idx)

    if status!=[]:
        posStat = QgsVectorLayer("point", "Status", "memory")
        prStat = posStat.dataProvider()
        fields=["Link_ID","Status/Setting"]; fieldsCode=[0,0]
        createColumnsAttrb(prStat,fields,fieldsCode)
        writeDBF(posStat,ppStat,prStat,saveFile,inpname, "_STATUS", iface,idx)

    if emitters!=[]:
        posEmit = QgsVectorLayer("point", "Emitters", "memory")
        prEmit = posEmit.dataProvider()
        fields=["Junc_ID","Coeff."]; fieldsCode=[0,1]
        createColumnsAttrb(prEmit,fields,fieldsCode)
        writeDBF(posEmit,ppEmit,prEmit,saveFile,inpname, "_EMITTERS", iface,idx)

    if controls!=[]:
        posCont = QgsVectorLayer("point", "Controls", "memory")
        prCont = posCont.dataProvider()
        fields=["Controls"]; fieldsCode=[0]
        createColumnsAttrb(prCont,fields,fieldsCode)
        writeDBF(posCont,ppCont,prCont,saveFile,inpname, "_CONTROLS", iface,idx)

    if patterns!=[]:
        posPat = QgsVectorLayer("point", "Patterns", "memory")
        prPat = posPat.dataProvider()
        fields=["Pattern_ID","Multipliers"]; fieldsCode=[0,0]
        createColumnsAttrb(prPat,fields,fieldsCode)
        writeDBF(posPat,ppPat,prPat,saveFile,inpname, "_PATTERNS", iface,idx)

    if curves[0]!=[]:
        posCurv = QgsVectorLayer("point", "Curves", "memory")
        prCurv = posCurv.dataProvider()
        fields=["Curve_ID","X-Value","Y-Value","Type"]; fieldsCode=[0,0,0,0]
        createColumnsAttrb(prCurv,fields,fieldsCode)
        writeDBF(posCurv,ppCurv,prCurv,saveFile,inpname, "_CURVES", iface,idx)


    # Write Valve Shapefile
    if d.getBinLinkValveCount()>0:
        posValve = QgsVectorLayer("point", "Valve", "memory")
        prValve = posValve.dataProvider()
        fields=["ID","NodeFrom","NodeTo","Diameter","Type","Setting","MinorLoss"]
        fieldsCode=[0,0,0,1,0,1,1]
        createColumnsAttrb(prValve,fields,fieldsCode)

        linkID=d.getBinLinkValveNameID()
        linkType=d.getBinLinkValveType()  # valve type
        linkDiameter=d.getBinLinkValveDiameters()
        linkInitSett=d.getBinLinkValveSetting() #BinLinkValveSetting
        linkMinorloss=d.getBinLinkValveMinorLoss()

        posValve.startEditing()
        for i, p in enumerate(d.getBinLinkValveIndex()):
            xx= (float(x1[p])+float(x2[p]))/2
            yy= (float(y1[p])+float(y2[p]))/2
            feature = QgsFeature()
            point = QgsPoint(xx,yy)
            feature.setGeometry(QgsGeometry.fromPoint(point))
            feature.setAttributes([linkID[i],ndlConn[0][p],ndlConn[1][p],linkDiameter[i],linkType[i],linkInitSett[i],linkMinorloss[i]])
            prValve.addFeatures([feature])
        QgsVectorFileWriter.writeAsVectorFormat(posValve,saveFile+"_valves"+'.shp',"utf-8",None,"ESRI Shapefile")
        ll=iface.addVectorLayer(saveFile+"_valves"+'.shp', inpname[:len(inpname)-4]+"_valves", "ogr")
        iface.legendInterface().moveLayer( ll, idx )

    # Write Pump Shapefile
    if d.getBinLinkPumpCount()>0:
        posPump = QgsVectorLayer("point", "Pump", "memory")
        prPump = posPump.dataProvider()
        fields=["ID","NodeFrom","NodeTo","Power","Pattern","Curve"]
        fieldsCode=[0,0,0,0,0,0]#,1,1]

        curveXY = d.getBinCurvesXY()
        curvesID = d.getBinCurvesNameID()

        a = curvesID
        b = []
        for l in a:
            if l not in b:
                b.append(l)
        curvesIDunique = b
        CurvesTmpIndices=[]
        for p in range(0, len(curvesIDunique)):
            CurvesTmpIndices.append(curvesID.count(curvesIDunique[p]))

        curveIndices=[]
        Curve=d.getBinLinkPumpCurveNameID()
        for i in range(len(Curve)):
            curveIndices.append(curvesIDunique.index(Curve[i]))
        if d.getBinCurveCount():
            CurvesTmpIndicesFinal=[]
            CurvesTmpIndicesFinal.append([ CurvesTmpIndices[index] for index in curveIndices ])

            CurvesTmp=[]
            i=0
            for u in range(max(CurvesTmpIndicesFinal[0])):
                fields.append('Head'+str(u+1)); fields.append('Flow'+str(u+1))
                fieldsCode.append(1); fieldsCode.append(1)
                if u<d.getBinCurveCount():
                    tmp1=[]
                    for p in range(CurvesTmpIndices[u]):
                        tmp1.append([curveXY[i][0], curveXY[i][1]])
                        i=i+1
                    CurvesTmp.append(tmp1)

        createColumnsAttrb(prPump,fields,fieldsCode)

        chPowerPump=d.getBinLinkPumpPower()
        pumpID = d.getBinLinkPumpNameID()
        patternsIDs=d.getBinLinkPumpPatterns()
        ppatt=d.getBinLinkPumpPatternsPumpID()
        linkID=d.getBinLinkNameID()

        posPump.startEditing()
        for i, p in enumerate(d.getBinLinkPumpIndex()):
            Curve=[];power=[];pattern=[]
            pumpNameIDPower=d.getBinLinkPumpNameIDPower()
            if len(pumpNameIDPower)>0:
                for uu in range(0,len(pumpNameIDPower)):
                    if pumpNameIDPower[uu]==pumpID[i]:
                        power=chPowerPump[uu]
            if len(patternsIDs)>0:
                for uu in range(0,len(ppatt)):
                    if ppatt[uu]==pumpID[i]:
                        pattern=patternsIDs[uu]

            xx= (float(x1[p])+float(x2[p]))/2
            yy= (float(y1[p])+float(y2[p]))/2
            feature = QgsFeature()
            point = QgsPoint(xx,yy)
            feature.setGeometry(QgsGeometry.fromPoint(point))

            if Curve==[]:
                Curve='NULL'
            if power==[]:
                power='NULL'
            if pattern==[]:
                pattern='NULL'

            if d.getBinCurveCount()>0 and len(pumpNameIDPower)==0:
                Curve=d.getBinLinkPumpCurveNameID()[i]
                curveIndex = curvesIDunique.index(Curve)

            feature.initAttributes(6+sum(CurvesTmpIndices)*2+1)
            feature.setAttribute(0, linkID[p])
            feature.setAttribute(1, ndlConn[0][p])
            feature.setAttribute(2, ndlConn[1][p])
            feature.setAttribute(3, power)
            feature.setAttribute(4, pattern)
            feature.setAttribute(5, Curve)

            if d.getBinCurveCount()==1:
                w=6
                for p in range(CurvesTmpIndices[curveIndex]):
                    print 6+sum(CurvesTmpIndices)
                    feature.setAttribute(w, CurvesTmp[curveIndex][p][0])
                    feature.setAttribute(w+1, CurvesTmp[curveIndex][p][1])
                    w=w+2

            for j in range(d.getBinCurveCount()-1):
                w=6
                for p in range(CurvesTmpIndices[curveIndex]):
                    feature.setAttribute(w, CurvesTmp[curveIndex][p][0])
                    feature.setAttribute(w+1, CurvesTmp[curveIndex][p][1])
                    w=w+2

            prPump.addFeatures([feature])
        QgsVectorFileWriter.writeAsVectorFormat(posPump,saveFile+"_pumps"+'.shp',"utf-8",None,"ESRI Shapefile")
        ll=iface.addVectorLayer(saveFile+"_pumps"+'.shp', inpname[:len(inpname)-4]+"_pumps", "ogr")
        iface.legendInterface().moveLayer( ll, idx )
    if d.getBinLinkPipeCount():
        QgsVectorFileWriter.writeAsVectorFormat(posPipe,saveFile+"_pipes"+'.shp',"utf-8",None,"ESRI Shapefile")
        ll=iface.addVectorLayer(saveFile+"_pipes"+'.shp', inpname[:len(inpname)-4]+"_pipes", "ogr")
        iface.legendInterface().moveLayer( ll, idx )
    if d.getBinNodeJunctionCount():
        QgsVectorFileWriter.writeAsVectorFormat(posJunction,saveFile+"_junctions"+'.shp',"utf-8",None,"ESRI Shapefile")
        ll=iface.addVectorLayer(saveFile+"_junctions"+'.shp', inpname[:len(inpname)-4]+"_junctions", "ogr")
        iface.legendInterface().moveLayer( ll, idx )
    if d.getBinNodeTankCount():
        QgsVectorFileWriter.writeAsVectorFormat(posTank,saveFile+"_tanks"+'.shp',"utf-8",None,"ESRI Shapefile")
        ll=iface.addVectorLayer(saveFile+"_tanks"+'.shp', inpname[:len(inpname)-4]+"_tanks", "ogr")
        iface.legendInterface().moveLayer( ll, idx )
    if d.getBinNodeReservoirCount():
        QgsVectorFileWriter.writeAsVectorFormat(posReservoirs,saveFile+"_reservoirs"+'.shp',"utf-8",None,"ESRI Shapefile")
        ll=iface.addVectorLayer(saveFile+"_reservoirs"+'.shp', inpname[:len(inpname)-4]+"_reservoirs", "ogr")
        iface.legendInterface().moveLayer( ll, idx )

    return idx

def writeDBF(pos,pp,pr,saveFile,inpname, param, iface,idx):
        pos.startEditing()
        for i in range(len(pp)):
            feat = QgsFeature()
            feat.setAttributes(pp[i])
            pr.addFeatures([feat])
        QgsVectorFileWriter.writeAsVectorFormat(pos,saveFile+param+'.dbf',"utf-8",None,"DBF file")
        ll=iface.addVectorLayer(saveFile+param+'.dbf', inpname[:len(inpname)-4]+param, "ogr")
        iface.legendInterface().moveLayer( ll, idx )

def createColumnsAttrb(pr,fields,fieldsCode):
    for i in range(len(fieldsCode)):
        if fieldsCode[i]==0:
            pr.addAttributes( [ QgsField(fields[i], QVariant.String) ] )
        else:
            pr.addAttributes( [ QgsField(fields[i], QVariant.Double, 'double', 20, 2) ] )

