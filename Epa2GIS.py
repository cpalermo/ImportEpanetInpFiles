#(C)Marios Kyriakou 2016
#University of Cyprus, KIOS Research Center for Intelligent Systems and Networks
import shapefile, os
import readEpanetFile as d
from qgis.core import QgsFeature,QgsVectorLayer,QgsVectorFileWriter
import qgis.utils
import time
from PyQt4.QtGui import QProgressBar
from qgis.gui import QgsMessageBar

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
        wO = shapefile.Writer(shapefile.POINT)
    if mixing!=[]:
        wMix = shapefile.Writer(shapefile.POINT)
        wMix.field('Tank_ID','C',254)
        wMix.field('Model','C',254)
        wMix.field('Fraction','N',20,9)
    if reactions!=[]:
        wReact = shapefile.Writer(shapefile.POINT)
        wReact.field('Type','C',254)
        wReact.field('Pipe/Tank','C',254)
        wReact.field('Coeff.','N',20,9)
    if sources!=[]:
        wSourc = shapefile.Writer(shapefile.POINT)
        wSourc.field('Node_ID','C',254)
        wSourc.field('Type','C',254)
        wSourc.field('Strength','N',20,9)
        wSourc.field('Pattern','C',254)
    if rules!=[] and len(rules[0])>3:
        wRul = shapefile.Writer(shapefile.POINT)
        wRul.field('Rule_ID','C',254)
        wRul.field('Rule','C',254)
    if quality!=[]:
        wQual = shapefile.Writer(shapefile.POINT)
        wQual.field('Node_ID','C',254)
        wQual.field('Init_Qual','N',20,9)
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
        wTimes = shapefile.Writer(shapefile.POINT)
    if energy!=[]:
        wE = shapefile.Writer(shapefile.POINT)
    if report!=[]:
        wRep = shapefile.Writer(shapefile.POINT)
    if options!=[]:
        wOpt = shapefile.Writer(shapefile.POINT)
    ppE=[];ppO=[];ppTimes=[];ppRep=[];ppOpt=[]

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
            wMix.point(0,0)
            if len(mixing[i])==3:
                wMix.record(mixing[i][0],mixing[i][1],mixing[i][2])
            else:
                wMix.record(mixing[i][0],mixing[i][1],0)
        if i<allSections[11]:
            wReact.point(0,0)
            wReact.record(reactions[i][0],reactions[i][1],reactions[i][2])
        if i<allSections[10]:
            wSourc.point(0,0);pat=''
            if len(sources[i])>3:
                pat = sources[i][3]
            wSourc.record(sources[i][0],sources[i][1],sources[i][2],pat)
        if i<allSections[9]:
            wRul.point(0,0)
            a = rules[i][1][0]+rules[i][2][0]+rules[i][3][0]
            wRul.record(rules[i][0][1][1],a)
        if i<allSections[8]:
            wQual.point(0,0)
            wQual.record(quality[i][0],quality[i][1])
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
                wE.field("Global",'C',254)
                if len(energy[i])>2:
                    ppE.append(energy[i][1]+' '+energy[i][2])
                else:
                    ppE.append(energy[i][1])
            if mm.upper()=="PUMP":
                wE.field("Pump",'C',254)
                if len(energy[i])>2:
                    ppE.append(energy[i][1]+' '+energy[i][2])
                else:
                    ppE.append(energy[i][1])
            elif mm.upper()=="DEMAND":
                if energy[i][1].upper()=="CHARGE":
                    wE.field("DemCharge",'C',254)
                    if len(energy[i])>2:
                        ppE.append(energy[i][2])
            wE.point(0,0)
        if i<allSections[1]:
            mm = optReactions[i][0]
            if mm.upper()=="ORDER":
                wO.field("Order",'C',254)
                if len(optReactions[i])>2:
                    ppO.append(optReactions[i][1]+' '+optReactions[i][2])
                else:
                    ppO.append(optReactions[i][1])
            elif mm.upper()=="GLOBAL":
                wO.field("Global",'C',254)
                if len(optReactions[i])>2:
                    ppO.append(optReactions[i][1]+' '+optReactions[i][2])
                else:
                    ppO.append(optReactions[i][1])
            elif mm.upper()=="BULK":
                wO.field("Bulk",'C',254)
                if len(optReactions[i])>2:
                    ppO.append(optReactions[i][1]+' '+optReactions[i][2])
                else:
                    ppO.append(optReactions[i][1])
            elif mm.upper()=="WALL":
                wO.field("Wall",'C',254)
                if len(optReactions[i])>2:
                    ppO.append(optReactions[i][1]+' '+optReactions[i][2])
                else:
                    ppO.append(optReactions[i][1])
            elif mm.upper()=="TANK":
                wO.field("Tank",'C',254)
                if len(optReactions[i])>2:
                    ppO.append(optReactions[i][1]+' '+optReactions[i][2])
                else:
                    ppO.append(optReactions[i][1])
            elif mm.upper()=="LIMITING":
                if optReactions[i][1].upper()=="POTENTIAL":
                    wO.field("LimPotent.",'C',254)
                    if len(optReactions[i])>2:
                        ppO.append(optReactions[i][2])
            elif mm.upper()=="ROUGHNESS":
                if optReactions[i][1].upper()=="CORRELATION":
                    wO.field("RoughCorr",'C',254)
                    if len(optReactions[i])>2:
                        ppO.append(optReactions[i][2])
            wO.point(0,0)
        if i<allSections[13]:
            mm = times[i][0]
            if mm.upper()=="DURATION":
                wTimes.field("Duration",'C',254)
                ppTimes.append(times[i][1])
            if mm.upper()=="HYDRAULIC":
                wTimes.field("HydStep",'C',254)
                ppTimes.append(times[i][2])
            elif mm.upper()=="QUALITY":
                wTimes.field("QualStep",'C',254)
                ppTimes.append(times[i][2])
            elif mm.upper()=="RULE":
                wTimes.field("RuleStep",'C',254)
                ppTimes.append(times[i][2])
            elif mm.upper()=="PATTERN":
                if times[i][1].upper()=="TIMESTEP":
                    wTimes.field("PatStep",'C',254)
                    ppTimes.append(times[i][2])
                if times[i][1].upper()=="START":
                    wTimes.field("PatStart",'C',254)
                    ppTimes.append(times[i][2])
            elif mm.upper()=="REPORT":
                if times[i][1].upper()=="TIMESTEP":
                    wTimes.field("RepStep",'C',254)
                    ppTimes.append(times[i][2])
                if times[i][1].upper()=="START":
                    wTimes.field("RepStart",'C',254)
                    ppTimes.append(times[i][2])
            elif mm.upper()=="START":
                if times[i][1].upper()=="CLOCKTIME":
                    wTimes.field("StartClock",'C',254)
                    if len(times[i])>3:
                        ppTimes.append(times[i][2]+' '+times[i][3])
                    else:
                        ppTimes.append(times[i][2])
            elif mm.upper()=="STATISTIC":
                wTimes.field("Statistic",'C',254)
                if times[i][1].upper()=='NONE' or times[i][1].upper()=='AVERAGE' or times[i][1].upper()=='MINIMUM' or times[i][1].upper()=='MAXIMUM' or times[i][1].upper()=='RANGE':
                    ppTimes.append(times[i][1])
            wTimes.point(0,0)
        if i<allSections[14]:
            mm = report[i][0]
            if mm.upper()=="PAGESIZE":
                wRep.field("PageSize",'C',254)
                ppRep.append(report[i][1])
            if mm.upper()=="FILE":
                wRep.field("FileName",'C',254)
                ppRep.append(report[i][1])
            elif mm.upper()=="STATUS":
                wRep.field("Status",'C',254)
                ppRep.append(report[i][1])
            elif mm.upper()=="SUMMARY":
                wRep.field("Summary",'C',254)
                ppRep.append(report[i][1])
            elif mm.upper()=="ENERGY":
                wRep.field("Energy",'C',254)
                ppRep.append(report[i][1])
            elif mm.upper()=="NODES":
                wRep.field("Nodes",'C',254)
                if len(report[i])>2:
                    ppRep.append(report[i][1]+' '+report[i][2])
                else:
                    ppRep.append(report[i][1])
            elif mm.upper()=="LINKS":
                wRep.field("Links",'C',254)
                if len(report[i])>2:
                    ppRep.append(report[i][1]+' '+report[i][2])
                else:
                    ppRep.append(report[i][1])
            else:
                wRep.field(mm,'C',254)
                if len(report[i])>2:
                    ppRep.append(report[i][1]+' '+report[i][2])
                else:
                    ppRep.append(report[i][1])
            wRep.point(0,0)
        if i<allSections[15]:
            mm = options[i][0]
            if mm.upper()=="UNITS":
                wOpt.field("Units",'C',254)
                ppOpt.append(options[i][1])
            if mm.upper()=="HYDRAULICS":
                wOpt.field("Hydraulics",'C',254)
                if len(options[i])>2:
                    ppOpt.append(options[i][1]+' '+options[i][2])
                else:
                    ppOpt.append(options[i][1])
            elif mm.upper()=="QUALITY":
                wOpt.field("Quality",'C',254)
                if len(options[i])>2:
                    ppOpt.append(options[i][1]+' '+options[i][2])
                elif len(options[i])>3:
                    ppOpt.append(options[i][1]+' '+options[i][2]+' '+options[i][3])
                else:
                    ppOpt.append(options[i][1])
            elif mm.upper()=="VISCOSITY":
                wOpt.field("Viscosity",'C',254)
                ppOpt.append(options[i][1])
            elif mm.upper()=="DIFFUSIVITY":
                wOpt.field("Diffusivity",'C',254)
                ppOpt.append(options[i][1])
            elif mm.upper()=="SPECIFIC":
                if options[i][1].upper()=="GRAVITY":
                    wOpt.field("SpecGrav",'C',254)
                    ppOpt.append(options[i][2])
            elif mm.upper()=="TRIALS":
                wOpt.field("Trials",'C',254)
                ppOpt.append(options[i][1])
            elif mm.upper()=="HEADLOSS":
                wOpt.field("Headloss",'C',254)
                ppOpt.append(options[i][1])
            elif mm.upper()=="ACCURACY":
                wOpt.field("Accuracy",'C',254)
                ppOpt.append(options[i][1])
            elif mm.upper()=="UNBALANCED":
                wOpt.field("Unbalanced",'C',254)
                if len(options[i])>2:
                    ppOpt.append(options[i][1]+' '+options[i][2])
                else:
                    ppOpt.append(options[i][1])
            elif mm.upper()=="PATTERN":
                wOpt.field("PatID",'C',254)
                ppOpt.append(options[i][1])
            elif mm.upper()=="TOLERANCE":
                wOpt.field("Tolerance",'C',254)
                ppOpt.append(options[i][1])
            elif mm.upper()=="MAP":
                wOpt.field("Map",'C',254)
                ppOpt.append(options[i][1])
            elif mm.upper()=="DEMAND":
                if options[i][1].upper()=="MULTIPLIER":
                    wOpt.field("DemMult",'C',254)
                    ppOpt.append(options[i][2])
            elif mm.upper()=="EMITTER":
                if options[i][1].upper()=="EXPONENT":
                    wOpt.field("EmitExp",'C',254)
                    ppOpt.append(options[i][2])
            elif mm.upper()=="CHECKFREQ":
                wOpt.field("CheckFreq",'C',254)
                ppOpt.append(options[i][1])
            elif mm.upper()=="MAXCHECK":
                wOpt.field("MaxCheck",'C',254)
                ppOpt.append(options[i][1])
            elif mm.upper()=="DAMPLIMIT":
                wOpt.field("DampLimit",'C',254)
                ppOpt.append(options[i][1])
            wOpt.point(0,0)


    if d.getBinNodeJunctionCount():
        wJunction.save(saveFile+'_junctions')
    if d.getBinLinkPipeCount():
        wpipe.save(saveFile+'_pipes')
    if d.getBinNodeTankCount():
        wTank.save(saveFile+'_tanks')
    if d.getBinNodeReservoirCount():
        wReservoirs.save(saveFile+'_reservoirs')

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

    pb.setValue(85)

    Sect = [0]*6
    Sect[0]=len(times)
    Sect[1]=len(report)
    Sect[2]=len(options)
    Sect[3]=len(energy)
    Sect[4]=len(reactions)
    if times!=[]:
        wTimes.save(saveFile+'_tempTIMES')
        posTimes = QgsVectorLayer(saveFile+'_tempTIMES.shp',"Layer Name","ogr")
        featTimes = QgsFeature()
        prTimes = posTimes.dataProvider()
        prTimes.addFeatures([featTimes])
    if options!=[]:
        wOpt.save(saveFile+'_tempOPTIONS')
        posOpt = QgsVectorLayer(saveFile+'_tempOPTIONS.shp',"Layer Name","ogr")
        featOpt = QgsFeature()
        prOpt = posOpt.dataProvider()
        prOpt.addFeatures([featOpt])
    if report!=[]:
        wRep.save(saveFile+'_tempREPORT')
        posRep = QgsVectorLayer(saveFile+'_tempREPORT.shp',"Layer Name","ogr")
        featRep = QgsFeature()
        prRep = posRep.dataProvider()
        prRep.addFeatures([featRep])
    if energy!=[]:
        wE.save(saveFile+'_tempENERGY')
        posE = QgsVectorLayer(saveFile+'_tempENERGY.shp',"Layer Name","ogr")
        featE = QgsFeature()
        prE = posE.dataProvider()
        prE.addFeatures([featE])
    if reactions!=[]:
        wO.save(saveFile+'_tempREACTIONS')
        posO = QgsVectorLayer(saveFile+'_tempREACTIONS.shp',"Layer Name","ogr")
        featO = QgsFeature()
        prO = posO.dataProvider()
        prO.addFeatures([featO])
        pb.setValue(100)
    for i in range(max(Sect)):
        updateMap={}
        if i<Sect[0]:
            updateMap[featTimes.id()] = {prTimes.fields().indexFromName(str(posTimes.pendingFields()[i].name())): ppTimes[i] }
            prTimes.changeAttributeValues( updateMap )
            if i==Sect[0]-1:
                QgsVectorFileWriter.writeAsVectorFormat(posTimes,saveFile+'_TIMES.dbf',"utf-8",None,"DBF file")
                ll=iface.addVectorLayer(saveFile+'_TIMES.dbf', inpname[:len(inpname)-4]+"_TIMES", "ogr")
                iface.legendInterface().moveLayer( ll, idx )
                #ll.loadNamedStyle(getPathPlugin+"white.qml")
        if i<Sect[2]:
            updateMap[featOpt.id()] = {prOpt.fields().indexFromName(str(posOpt.pendingFields()[i].name())): ppOpt[i] }
            prOpt.changeAttributeValues( updateMap )
            if i==Sect[2]-1:
                QgsVectorFileWriter.writeAsVectorFormat(posOpt,saveFile+'_OPTIONS.dbf',"utf-8",None,"DBF file")
                ll=iface.addVectorLayer(saveFile+"_OPTIONS"+'.dbf', inpname[:len(inpname)-4]+"_OPTIONS", "ogr")
                iface.legendInterface().moveLayer( ll, idx )
                #ll.loadNamedStyle(getPathPlugin+"white.qml")
        if i<Sect[1]:
            updateMap[featRep.id()] = {prRep.fields().indexFromName(str(posRep.pendingFields()[i].name())): ppRep[i] }
            prRep.changeAttributeValues( updateMap )
            if i==Sect[1]-1:
                QgsVectorFileWriter.writeAsVectorFormat(posRep,saveFile+'_REPORT.dbf',"utf-8",None,"DBF file")
                ll=iface.addVectorLayer(saveFile+"_REPORT"+'.dbf', inpname[:len(inpname)-4]+"_REPORT", "ogr")
                iface.legendInterface().moveLayer( ll, idx )
                #ll.loadNamedStyle(getPathPlugin+"white.qml")
        if i<Sect[3]:
            updateMap[featE.id()] = {prE.fields().indexFromName(str(posE.pendingFields()[i].name())): ppE[i] }
            prE.changeAttributeValues( updateMap )
            if i==Sect[3]-1:
                QgsVectorFileWriter.writeAsVectorFormat(posE,saveFile+'_ENERGY.dbf',"utf-8",None,"DBF file")
                ll=iface.addVectorLayer(saveFile+"_ENERGY"+'.dbf', inpname[:len(inpname)-4]+"_ENERGY", "ogr")
                iface.legendInterface().moveLayer( ll, idx )
                #ll.loadNamedStyle(getPathPlugin+"white.qml")
        if i<Sect[4]:
            updateMap[featO.id()] = {prO.fields().indexFromName(str(posO.pendingFields()[i].name())): ppO[i] }
            prO.changeAttributeValues( updateMap )
            if i==Sect[4]-1:
                QgsVectorFileWriter.writeAsVectorFormat(posO,saveFile+'_REACTIONS.dbf',"utf-8",None,"DBF file")
                ll=iface.addVectorLayer(saveFile+"_REACTIONS"+'.dbf', inpname[:len(inpname)-4]+"_REACTIONS", "ogr")
                iface.legendInterface().moveLayer( ll, idx )
                #ll.loadNamedStyle(getPathPlugin+"white.qml")

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
    if quality!=[]:
        wQual.save(saveFile+'_temp')
        writeDBF(saveFile,inpname,"_QUALITY",rr,iface,wQual,idx); del wQual
    if rules!=[] and len(rules[0])>3:
        wRul.save(saveFile+'_temp')
        writeDBF(saveFile,inpname,"_RULES",rr,iface,wRul,idx); del wRul
    if sources!=[]:
        wSourc.save(saveFile+'_temp')
        writeDBF(saveFile,inpname,"_SOURCES",rr,iface,wSourc,idx); del wSourc
    if reactions!=[]:
        wReact.save(saveFile+'_temp')
        writeDBF(saveFile,inpname,"_REACTIONSinfo",rr,iface,wReact,idx); del wReact
    if mixing!=[]:
        wMix.save(saveFile+'_temp')
        writeDBF(saveFile,inpname,"_MIXING",rr,iface,wMix,idx); del wMix

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
