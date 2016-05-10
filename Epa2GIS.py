#(C)Marios Kyriakou 2016
#University of Cyprus, KIOS Research Center for Intelligent Systems and Networks
import shapefile, os
import readEpanetFile as d
from qgis.core import QgsFeature,QgsVectorLayer,QgsVectorFileWriter, QgsField
import qgis.utils
from PyQt4.QtGui import QProgressBar
from qgis.gui import QgsMessageBar
from PyQt4.QtCore import QVariant

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
    msgBar= iface.messageBar()
    pb= QProgressBar()
    msgBar.pushWidget(pb, QgsMessageBar().INFO, 5)
    pb.setValue(1)
    d.BinUpdateClass(pb)
    nlinkCount=d.getBinLinkCount()
    res = newpath + '\\'
    saveFile=res+inpname[:len(inpname)-4]

    pb.setValue(14)
    #iface.messageBar().clearWidgets()

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
    allSections=[0]*20
    allSections[0]=len(energy)
    allSections[1]=len(optReactions)
    allSections[2]=len(demands)
    allSections[3]=len(status)
    allSections[4]=len(emitters)
    allSections[5]=len(controls)
    allSections[6]=len(patterns)
    allSections[7]=len(curves[0])
    allSections[8]=len(quality)
    allSections[9]=len(rules)
    allSections[10]=len(sources)
    allSections[11]=len(reactions)
    allSections[12]=len(mixing)
    allSections[13]=len(times)
    allSections[14]=len(report)
    allSections[15]=len(options)
    allSections[16]=d.getBinNodeCount()
    allSections[17]=d.getBinLinkCount()
    ss=max(allSections)

    idx = iface.legendInterface().addGroup(inpname[:len(inpname)-4])

    xy=d.getBinNodeCoordinates()
    pb.setValue(15)
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
    pb.setValue(16)

    #Get data of Junctions
    if d.getBinNodeJunctionCount()>0:
        # Write Junction Shapefile
        wJunction = shapefile.Writer(shapefile.POINT)
        wJunction.field('dc_id','C',254)
        wJunction.field('elevation','N',20)
        wJunction.field('pattern','C',254)
        wJunction.field('demand','N',20,9)
        ndEle=d.getBinNodeJunctionElevations()
        ndBaseD=d.getBinNodeBaseDemands()
        ndID=d.getBinNodeNameID()
        ndPatID=d.getBinNodeDemandPatternID()

    #Get data of Pipes
    #Write shapefile pipe
    if nlinkCount>0:
        wpipe = shapefile.Writer(shapefile.POLYLINE)
        wpipe.field('dc_id','C',254)
        wpipe.field('node1','C',254)
        wpipe.field('node2','C',254)
        wpipe.field('length','N',20,9)
        wpipe.field('diameter','N',20,9)
        wpipe.field('status','C',254)
        wpipe.field('roughness','N',20,9)
        wpipe.field('minorloss','N',20,9)
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
        wTank = shapefile.Writer(shapefile.POINT)
        wTank.field('dc_id','C',254)
        wTank.field('elevation','N',20)
        wTank.field('initiallev','N',20)
        wTank.field('minimumlev','N',20)
        wTank.field('maximumlev','N',20)
        wTank.field('diameter','N',20)
        wTank.field('minimumvol','N',20)
        wTank.field('volumecurv','N',20)
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
        wReservoirs = shapefile.Writer(shapefile.POINT)
        wReservoirs.field('dc_id','C',254)
        wReservoirs.field('head','N',20)
        head=d.getBinNodeReservoirElevations()

    if optReactions!=[]:
        posO = QgsVectorLayer("point", "Times", "memory")
        prO = posO.dataProvider()
    if mixing!=[]:
        posMix = QgsVectorLayer("point", "Mixing", "memory")
        prMix = posMix.dataProvider()
        prMix.addAttributes( [ QgsField("Tank_ID", QVariant.String) ] )
        prMix.addAttributes( [ QgsField("Model", QVariant.String) ] )
        prMix.addAttributes( [ QgsField("Fraction", QVariant.Double) ] )
    if reactions!=[]:
        posReact = QgsVectorLayer("point", "ReactionsInfo", "memory")
        prReact = posReact.dataProvider()
        prReact.addAttributes( [ QgsField("Type", QVariant.String) ] )
        prReact.addAttributes( [ QgsField("Pipe/Tank", QVariant.String) ] )
        prReact.addAttributes( [ QgsField("Coeff.", QVariant.Double) ] )
    if sources!=[]:
        posSourc = QgsVectorLayer("point", "Sources", "memory")
        prSourc = posSourc.dataProvider()
        prSourc.addAttributes( [ QgsField("Node_ID", QVariant.String) ] )
        prSourc.addAttributes( [ QgsField("Type", QVariant.String) ] )
        prSourc.addAttributes( [ QgsField("Strength", QVariant.Double) ] )
        prSourc.addAttributes( [ QgsField("Pattern", QVariant.String) ] )
    if rules!=[] and len(rules[0])>3:
        posRul = QgsVectorLayer("point", "Sources", "memory")
        prRul = posRul.dataProvider()
        prRul.addAttributes( [ QgsField("Rule_ID", QVariant.String) ] )
        prRul.addAttributes( [ QgsField("Rule", QVariant.String) ] )
    if quality!=[]:
        posQual = QgsVectorLayer("point", "Sources", "memory")
        prQual = posQual.dataProvider()
        prQual.addAttributes( [ QgsField("Node_ID", QVariant.String) ] )
        prQual.addAttributes( [ QgsField("Init_Qual", QVariant.Double) ] )
    if curves[0]!=[]:
        wCurv = shapefile.Writer(shapefile.POINT)
        wCurv.field('Curve_ID','C',254)
        wCurv.field('X-Value','C',254)
        wCurv.field('Y-Value','C',254)
        wCurv.field('Type','C',254)
    if patterns!=[]:
        wPat = shapefile.Writer(shapefile.POINT)
        wPat.field('Pattern_ID','C',254)
        wPat.field('Multipliers','C',254)
    if controls!=[]:
        wCont = shapefile.Writer(shapefile.POINT)
        wCont.field('Controls','C',254)
    if emitters!=[]:
        wEmit = shapefile.Writer(shapefile.POINT)
        wEmit.field('Junc_ID','C',254)
        wEmit.field('Coeff.','N',20,9)
    if status!=[]:
        wStat = shapefile.Writer(shapefile.POINT)
        wStat.field('Link_ID','C',254)
        wStat.field('Status/Setting','C',254)
    if demands!=[]:
        wDem = shapefile.Writer(shapefile.POINT)
        wDem.field('ID','C',254)
        wDem.field('Demand','N',20,9)
        wDem.field('Pattern','C',254)
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

    ppE=[];ppO=[];ppTimes=[];ppRep=[];ppOpt=[]
    ppMix=[];ppReactions=[];ppSourc=[];ppRul=[]
    ppQual=[]
    vvLink=68;bbLink=1
    for i in range(ss):
        if i<d.getBinNodeJunctionCount():
            wJunction.point(float(x[i]), float(y[i]))
            wJunction.record(ndID[i],ndEle[i],ndPatID[i],ndBaseD[i])
        if i<nlinkCount:
                if len(stat)==i:
                    ch=1
                if ch==1:
                    stat.append('OPEN')

                if i==nlinkCount/vvLink and vvLink>-1:
                    vvLink=vvLink-1
                    pb.setValue(18+bbLink); bbLink=bbLink+1

                x1.append(x[ndID.index(d.getBinLinkFromNode()[i])])
                y1.append(y[ndID.index(d.getBinLinkFromNode()[i])])
                x2.append(x[ndID.index(d.getBinLinkToNode()[i])])
                y2.append(y[ndID.index(d.getBinLinkToNode()[i])])

                if i in pIndex:
                    xx= (float(x1[i])+float(x2[i]))/2
                    yy= (float(y1[i])+float(y2[i]))/2
                    for p in range(0,2):
                        XY=[]
                        if p==0:
                            linkIDFinal=linkID[i]+'_pump1'
                            node1=ndlConn[0][i]
                            node2=linkIDFinal
                            indN1 = d.getBinNodeIndex(node1)
                            XY.append(([float(x[indN1]),float(y[indN1])],[xx,yy]))
                        elif p==1:
                            linkIDFinal=linkID[i]+'_pump2'
                            node1=linkIDFinal
                            node2=ndlConn[1][i]
                            indN2 = d.getBinNodeIndex(node2)
                            XY.append(([xx,yy],[float(x[indN2]),float(y[indN2])]))
                        length=0
                        diameter=0
                        roughness=0
                        minorloss=0
                        wpipe.line(parts=[XY[0]])
                        wpipe.record(linkIDFinal,node1,node2,length,diameter,stat[i],roughness,minorloss)
                elif i in vIndex:
                    xx= (float(x1[i])+float(x2[i]))/2
                    yy= (float(y1[i])+float(y2[i]))/2
                    for v in range(0,2):
                        XY=[]
                        if v==0:
                            linkIDFinal=linkID[i]+'_valve1'
                            node1=ndlConn[0][i]
                            node2=linkIDFinal
                            indN1 = d.getBinNodeIndex(node1)
                            XY.append(([float(x[indN1]),float(y[indN1])],[xx,yy]))
                        elif v==1:
                            linkIDFinal=linkID[i]+'_valve2'
                            node1=linkIDFinal
                            node2=ndlConn[1][i]
                            indN2 = d.getBinNodeIndex(node2)

                            XY.append(([xx,yy],[float(x[indN2]),float(y[indN2])]))
                        length=0
                        diameter=0
                        roughness=0
                        minorloss=0
                        wpipe.line(parts=[XY[0]])
                        wpipe.record(linkIDFinal,node1,node2,length,diameter,stat[i],roughness,minorloss)
                else:
                    point1 = [float(x1[i]),float(y1[i])]
                    point2 = [float(x2[i]),float(y2[i])]
                    if vertx[i]!=[]:
                        parts=[]
                        parts.append(point1)
                        for mm in range(len(vertxyFinal[kk])):
                            parts.append(vertxyFinal[kk][mm])
                        parts.append(point2)
                        wpipe.line(parts=[parts])
                        kk=kk+1
                    else:
                        wpipe.line(parts=[[[float(x1[i]),float(y1[i])],[float(x2[i]),float(y2[i])]]])
                    wpipe.record(linkID[i],ndlConn[0][i],ndlConn[1][i],linkLengths[i],linkDiameters[i],stat[i],linkRough[i],linkMinorloss[i])

        if i<d.getBinNodeTankCount():
            p=d.getBinNodeTankIndex()[i]-1
            wTank.point(float(x[p]), float(y[p]))
            wTank.record(ndTankID[i],ndTankelevation[i],initiallev[i],minimumlev[i],maximumlev[i],diameter[i],minimumvol[i],volumecurv[i])

        if i<d.getBinNodeReservoirCount():
            p=d.getBinNodeReservoirIndex()[i]-1
            wReservoirs.point(float(x[p]), float(y[p]))
            wReservoirs.record(ndID[p],head[i])

        if i<allSections[12]:
            if len(mixing[i])==3:
                ppMix.append([mixing[i][0],mixing[i][1],mixing[i][2]])
            else:
                ppMix.append([mixing[i][0],mixing[i][1]])
        if i<allSections[11]:
            ppReactions.append([reactions[i][0],reactions[i][1],reactions[i][2]])
        if i<allSections[10]:
            ppSourc.append([sources[i][0],sources[i][1]])
            if len(sources[i])>3:
                ppSourc.append([sources[i][0],sources[i][1],sources[i][3]])
        if i<allSections[9]:
            ppRul.append([rules[i][0][1][1],rules[i][1][0]+rules[i][2][0]+rules[i][3][0]])
        if i<allSections[8]:
            ppQual.append([quality[i][0],quality[i][1]])
        if i<allSections[7]:
            wCurv.point(0,0)
            wCurv.record(str(curves[0][i][0]),str(curves[0][i][1]),str(curves[0][i][2]),str(curves[1][i]))
        if i<allSections[6]:
            wPat.point(0,0)
            wPat.record(patterns[i][0],str(patterns[i][1]))
        if i<allSections[5]:
            wCont.point(0,0)
            wCont.record(controls[i])
        if i<allSections[4]:
            wEmit.point(0,0)
            wEmit.record(emitters[i][0],emitters[i][1])
        if i<allSections[3]:
            wStat.point(0,0)
            wStat.record(status[i][0],status[i][1])
        if i<allSections[2]:
            wDem.point(0,0)
            wDem.record(demands[i][0],demands[i][1],demands[i][2])
        if i<allSections[0]:
            mm = energy[i][0]
            if mm.upper()=="GLOBAL":
                prE.addAttributes( [ QgsField("Global", QVariant.String) ] )
                if len(energy[i])>2:
                    ppE.append(energy[i][1]+' '+energy[i][2])
                else:
                    ppE.append(energy[i][1])
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
                prO.addAttributes( [ QgsField("Order", QVariant.String) ] )
                if len(optReactions[i])>2:
                    ppO.append(optReactions[i][1]+' '+optReactions[i][2])
                else:
                    ppO.append(optReactions[i][1])
            elif mm.upper()=="GLOBAL":
                prO.addAttributes( [ QgsField("Global", QVariant.String) ] )
                if len(optReactions[i])>2:
                    ppO.append(optReactions[i][1]+' '+optReactions[i][2])
                else:
                    ppO.append(optReactions[i][1])
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


    if d.getBinNodeJunctionCount():
        wJunction.save(saveFile+'_junctions')
    if d.getBinLinkPipeCount():
        wpipe.save(saveFile+'_pipes')
    if d.getBinNodeTankCount():
        wTank.save(saveFile+'_tanks')
    if d.getBinNodeReservoirCount():
        wReservoirs.save(saveFile+'_reservoirs')

    if options!=[]:
        writeDBF2(posOpt,[ppOpt],prOpt,saveFile,inpname, "_OPTIONS", iface,idx)

    if report!=[]:
        writeDBF2(posRep,[ppRep],prRep,saveFile,inpname, "_REPORT", iface,idx)

    if times!=[]:
        writeDBF2(posTimes,[ppTimes],prTimes,saveFile,inpname, "_TIMES", iface,idx)

    if energy!=[]:
        writeDBF2(posE,[ppE],prE,saveFile,inpname, "_ENERGY", iface,idx)

    if optReactions!=[]:
        writeDBF2(posO,[ppO],prO,saveFile,inpname, "_REACTIONS", iface,idx)

    if mixing!=[]:
        writeDBF2(posMix,ppMix,prMix,saveFile,inpname, "_MIXING", iface,idx)

    if reactions!=[]:
        writeDBF2(posReact,ppReactions,prReact,saveFile,inpname, "_REACTIONSinfo", iface,idx)

    if sources!=[]:
        writeDBF2(posSourc,ppSourc,prSourc,saveFile,inpname, "_SOURCES", iface,idx)

    if rules!=[] and len(rules[0])>3:
        writeDBF2(posRul,ppRul,prRul,saveFile,inpname, "_RULES", iface,idx)

    if ppQual!=[]:
        #print ppQual
        writeDBF2(posQual,ppQual,prQual,saveFile,inpname, "_QUALITY", iface,idx)


    # Write Valve Shapefile
    if d.getBinLinkValveCount()>0:
        wValve = shapefile.Writer(shapefile.POINT)
        wValve.field('dc_id','C',254)
        wValve.field('node1','C',254)
        wValve.field('node2','C',254)
        wValve.field('diameter','N',20,9)
        wValve.field('type','C',254)
        wValve.field('setting','N',20,9)
        wValve.field('minorloss','N',20,9)
        linkID=d.getBinLinkValveNameID()
        linkType=d.getBinLinkValveType()  # valve type
        linkDiameter=d.getBinLinkValveDiameters()
        linkInitSett=d.getBinLinkValveSetting() #BinLinkValveSetting
        linkMinorloss=d.getBinLinkValveMinorLoss()
        for i, p in enumerate(d.getBinLinkValveIndex()):
            xx= (float(x1[p])+float(x2[p]))/2
            yy= (float(y1[p])+float(y2[p]))/2
            wValve.point(xx,yy)
            wValve.record(linkID[i],ndlConn[0][p],ndlConn[1][p],linkDiameter[i],linkType[i],linkInitSett[i],linkMinorloss[i])
        wValve.save(saveFile+'_valves')

    pb.setValue(70)

    # Write Pump Shapefile
    w = shapefile.Writer(shapefile.POINT)
    w.field('dc_id','C',254)
    w.field('node1','C',254)
    w.field('node2','C',254)
    w.field('head','C',254)
    w.field('flow','C',254)
    w.field('power','C',254)
    w.field('pattern','C',254)
    w.field('curveID','C',254)

    if d.getBinLinkPumpCount()>0:
        chPowerPump=d.getBinLinkPumpPower()
        cheadpump = d.getBinLinkPumpCurveNameID()
        pumpID = d.getBinLinkPumpNameID()
        patternsIDs=d.getBinLinkPumpPatterns()
        ppatt=d.getBinLinkPumpPatternsPumpID()
        linkID=d.getBinLinkNameID()
        for i, p in enumerate(d.getBinLinkPumpIndex()):
            Head=[];Flow=[];Curve=[];power=[];pattern=[]
            pumpNameIDPower=d.getBinLinkPumpNameIDPower()
            if len(pumpNameIDPower)>0:
                for uu in range(0,len(pumpNameIDPower)):
                    if pumpNameIDPower[uu]==pumpID[i]:
                        power=chPowerPump[uu]
            if len(patternsIDs)>0:
                for uu in range(0,len(ppatt)):
                    if ppatt[uu]==pumpID[i]:
                        pattern=patternsIDs[uu]

            if d.getBinCurveCount()>0 and len(pumpNameIDPower)==0:
                curveXY = d.getBinCurvesXY()
                curvesID = d.getBinCurvesNameID()
                for uu in range(0,len(curveXY)):
                    if curvesID[uu]==cheadpump[i]:
                        Head.append(str(curveXY[uu][0]))
                        Flow.append(str(curveXY[uu][1]))
                Curve=d.getBinLinkPumpCurveNameID()[i]
                xx= (float(x1[p])+float(x2[p]))/2
                yy= (float(y1[p])+float(y2[p]))/2
                w.point(xx,yy)
                wpipe.line(parts=[[[float(x1[p]),float(y1[p])],[float(x2[p]),float(y2[p])]]])

            else:
                xx= (float(x1[p])+float(x2[p]))/2
                yy= (float(y1[p])+float(y2[p]))/2
                w.point(xx,yy)
                wpipe.line(parts=[[[float(x1[p]),float(y1[p])],[float(x2[p]),float(y2[p])]]])
            Head = ' '.join(Head)
            Flow = ' '.join(Flow)
            if Head==[]:
                Head='NULL'
            if Flow==[]:
                Flow='NULL'
            if Curve==[]:
                Curve='NULL'
            if power==[]:
                power='NULL'
            if pattern==[]:
                pattern='NULL'
            w.record(linkID[p],ndlConn[0][p],ndlConn[1][p],Head,Flow,power,pattern,Curve)
        w.save(saveFile+'_pumps')

    # Create DBF files
    rr=newpath + '/'+inpname[:len(inpname)-4]
    pb.setValue(100)

    if demands!=[]:
        wDem.save(saveFile+'_temp')
        writeDBF(saveFile,inpname,"_DEMANDS",rr,iface,wCont,idx); del wDem
    if status!=[]:
        wStat.save(saveFile+'_temp')
        writeDBF(saveFile,inpname,"_STATUS",rr,iface,wCont,idx); del wStat
    if emitters!=[]:
        wCont.save(saveFile+'_temp')
        writeDBF(saveFile,inpname,"_EMITTERS",rr,iface,wCont,idx); del wCont
    if controls!=[]:
        wCont.save(saveFile+'_temp')
        writeDBF(saveFile,inpname,"_CONTROLS",rr,iface,wCont,idx); del wCont
    if patterns!=[]:
        wPat.save(saveFile+'_temp')
        writeDBF(saveFile,inpname,"_PATTERNS",rr,iface,wPat,idx); del wPat
    if curves[0]!=[]:
        wCurv.save(saveFile+'_temp')
        writeDBF(saveFile,inpname,"_CURVES",rr,iface,wCurv,idx); del wCurv

    return idx

def writeDBF(saveFile,inpname,param,rr,iface,w,idx):
    pos_dbf = QgsVectorLayer(saveFile+'_temp.shp',"Layer Name","ogr")
    QgsVectorFileWriter.writeAsVectorFormat(pos_dbf,saveFile+param+'.dbf',"utf-8",None,"DBF file")
    del pos_dbf # remove from memory - close file
    ll=iface.addVectorLayer(saveFile+param+'.dbf', inpname[:len(inpname)-4]+param, "ogr")
    iface.legendInterface().moveLayer( ll, idx )
    try:
        os.remove(rr+param+'.cpg')
    except:
        pass

def writeDBF2(pos,pp,pr,saveFile,inpname, param, iface,idx):
        pos.startEditing()
        for i in range(len(pp)):
            feat = QgsFeature()
            feat.setAttributes(pp[i])
            pr.addFeatures([feat])
        QgsVectorFileWriter.writeAsVectorFormat(pos,saveFile+param+'.dbf',"utf-8",None,"DBF file")
        ll=iface.addVectorLayer(saveFile+param+'.dbf', inpname[:len(inpname)-4]+param, "ogr")
        iface.legendInterface().moveLayer( ll, idx )