#(C)Marios Kyriakou 2016
#University of Cyprus, KIOS Research Center for Intelligent Systems and Networks
import shapefile, os
import readEpanetFile as d

def epaShp(inpname):
    file_extension = os.path.dirname(inpname)
    inpname = os.path.basename(inpname)
    inp = file_extension + '/'+ inpname
    if len(file_extension)==0:
        inp = inpname
    newpath = file_extension + '/_shapefiles_'
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    d.LoadFile(inp)
    d.BinUpdateClass()
    nlinkCount=d.getBinLinkCount()
    res = newpath + '\\'
    # Write Junction Shapefile
    w = shapefile.Writer(shapefile.POINT)
    w.autoBalance = 1
    w.field('dc_id','C',254)
    w.field('elevation','N',20)
    w.field('pattern','C',254)
    w.field('demand','N',20,9)

    xy=d.getBinNodeCoordinates()

    x=xy[0]
    y=xy[1]
    x1=xy[2]
    x2=xy[4]
    y1=xy[3]
    y2=xy[5]
    vertx=xy[6]
    verty=xy[7]
    vertxyFinal=[]
    for i in range(len(vertx)):
        vertxy=[]
        for u in range(len(vertx[i])):
            vertxy.append([float(vertx[i][u]),float(verty[i][u])])
        if vertxy!=[]:
            vertxyFinal.append(vertxy)

    if d.getBinNodeJunctionCount()>0:
        ndEle=d.getBinNodeJunctionElevations()
        ndBaseD=d.getBinNodeBaseDemands()
        ndID=d.getBinNodeNameID()
        ndPatID=d.getBinNodeDemandPatternID()
        for i in range(0,d.getBinNodeJunctionCount()):
            w.point(float(x[i]), float(y[i]))
            w.record(ndID[i],ndEle[i],ndPatID[i],ndBaseD[i])
        w.save(res+inpname[:len(inpname)-4]+'_junctions')

    # Write Pipe Shapefile
    wpipe = shapefile.Writer(shapefile.POLYLINE)
    wpipe.field('dc_id','C',254)
    wpipe.field('node1','C',254)
    wpipe.field('node2','C',254)
    wpipe.field('length','N',20,9)
    wpipe.field('diameter','N',20,9)
    wpipe.field('status','C',254)
    wpipe.field('roughness','N',20,9)
    wpipe.field('minorloss','N',20,9)
    wpipe.autoBalance = 1
    parts=[]
    pIndex = d.getBinLinkPumpIndex()
    vIndex = d.getBinLinkValveIndex()

    ndlConn=d.getBinNodesConnectingLinksID()
    if nlinkCount>0:
        stat=d.getBinLinkInitialStatus()
        kk=0
        for i in range(0,nlinkCount):
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
                linkID=d.getBinLinkNameID()
                linkLengths=d.getBinLinkLength()
                linkDiameters=d.getBinLinkDiameter()
                linkRough=d.getBinLinkRoughnessCoeff()
                linkMinorloss=d.getBinLinkMinorLossCoeff()
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
        wpipe.save(res+inpname[:len(inpname)-4]+'_pipes')

    # Write Tank Shapefile
    w = shapefile.Writer(shapefile.POINT)
    w.autoBalance = 1
    w.field('dc_id','C',254)
    w.field('elevation','N',20)
    w.field('initiallev','N',20)
    w.field('minimumlev','N',20)
    w.field('maximumlev','N',20)
    w.field('diameter','N',20)
    w.field('minimumvol','N',20)
    w.field('volumecurv','N',20)

    if d.getBinNodeTankCount()>0:
        ndTankelevation=d.getBinNodeTankElevations()
        initiallev=d.getBinNodeTankInitialLevel()
        minimumlev=d.getBinNodeTankMinimumWaterLevel()
        maximumlev=d.getBinNodeTankMaximumWaterLevel()
        diameter=d.getBinNodeTankDiameter()
        minimumvol=d.getBinNodeTankMinimumWaterVolume()
        volumecurv=d.getBinNodeTankVolumeCurveID()
        ndID=d.getBinNodeTankNameID()
        for i, tankindex in enumerate(d.getBinNodeTankIndex()):
            p=tankindex-1
            w.point(float(x[p]), float(y[p]))
            w.record(ndID[i],ndTankelevation[i],initiallev[i],minimumlev[i],maximumlev[i],diameter[i],minimumvol[i],volumecurv[i])
        w.save(res+inpname[:len(inpname)-4]+'_tanks')


    # Write Reservoir Shapefile
    w = shapefile.Writer(shapefile.POINT)
    w.autoBalance = 1
    w.field('dc_id','C',254)
    w.field('head','N',20)

    if d.getBinNodeReservoirCount()>0:
        head=d.getBinNodeReservoirElevations()
        ndID=d.getBinNodeNameID()
        for i, nodereservoirindex in enumerate(d.getBinNodeReservoirIndex()):
            p=nodereservoirindex-1
            w.point(float(x[p]), float(y[p]))
            w.record(ndID[p],head[i])
        w.save(res+inpname[:len(inpname)-4]+'_reservoirs')

    # Write Pump Shapefile
    w = shapefile.Writer(shapefile.POINT)
    w.autoBalance = 1
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
                        Head.append(curveXY[uu][0])
                        Flow.append(curveXY[uu][1])
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
        w.save(res+inpname[:len(inpname)-4]+'_pumps')

    # Write Valve Shapefile
    w = shapefile.Writer(shapefile.POINT)
    w.autoBalance = 1
    w.field('dc_id','C',254)
    w.field('node1','C',254)
    w.field('node2','C',254)
    w.field('diameter','N',20,9)
    w.field('type','C',254)
    w.field('setting','N',20,9)
    w.field('minorloss','N',20,9)

    if d.getBinLinkValveCount()>0:
        linkID=d.getBinLinkValveNameID()
        linkType=d.getBinLinkValveType()  # valve type
        linkDiameter=d.getBinLinkValveDiameters()
        linkInitSett=d.getBinLinkValveSetting() #BinLinkValveSetting
        linkMinorloss=d.getBinLinkValveMinorLoss()
        for i, p in enumerate(d.getBinLinkValveIndex()):
            xx= (float(x1[p])+float(x2[p]))/2
            yy= (float(y1[p])+float(y2[p]))/2
            w.point(xx,yy)
            w.record(linkID[i],ndlConn[0][p],ndlConn[1][p],linkDiameter[i],linkType[i],linkInitSett[i],linkMinorloss[i])
        w.save(res+inpname[:len(inpname)-4]+'_valves')

