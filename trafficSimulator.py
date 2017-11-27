#!/usr/bin/python3
from Map import point,carstatus
from Device import Car,Light
from copy import deepcopy
import time
import os

class trafficSimulator():
    def __init__(self,msize,maxc,sleepInt):
        self.currentCycle = 0
        self.maxCycle = maxc
        self.mapSize = msize
        self.sleepInterval = sleepInt
        self.carList = []
        self.lightList = []
        self.carStatusBuff = []
        self.simulatorMap = [ [ point() for i in range(msize)] for i in range(msize) ]
        self.carSightRange = 3

        for i in range(msize):
            for j in range(msize):
                self.simulatorMap[i][j].setCordinate(i,j)

    def buildMap(self):
        self.addRoad(1,0,1,30,3)
        self.addRoad(7,2,7,23,3)
        self.addRoad(13,0,13,30,1)
        self.addRoad(17,3,17,12,1)
        self.addRoad(18,12,18,30,3)
        self.addRoad(23,0,23,30,3)
        self.addRoad(26,8,26,23,1)
        self.addRoad(0,2,30,2,2)
        self.addRoad(1,6,13,6,0)
        self.addRoad(13,8,30,8,2)
        self.addRoad(0,12,30,12,0)
        self.addRoad(13,18,23,18,0)
        self.addRoad(0,23,30,23,2)
        self.addRoad(18,25,30,25,2)
        self.addRoad(1,27,18,27,0)
    def addRoad(self,startx,starty,endx,endy,d):
        if startx==endx:
            for i in range(starty,endy+1):
                self.simulatorMap[startx][i].addRoadDirecs(d)
        else:
            for i in range(startx,endx+1):
                self.simulatorMap[i][starty].addRoadDirecs(d)
    def createLights(self):
        #def __init__(self,x,y,devid,r,trafficmap):
        lightnum = 0
        for i in range(self.mapSize):
            for j in range(self.mapSize):
                if self.simulatorMap[i][j].getRoadDirecNum()>1:
                    self.lightList.append(Light(i,j,lightnum,6,self.simulatorMap))
    def createCars(self):
        #def __init__(self,x,y,devid,maxv,destx,desty,trafficmap):
        self.carList.append(Car(6,2,0,3,11,27,self.simulatorMap))
        self.simulatorMap[6][2].addCarID(0)
        self.carStatusBuff.append(carstatus(0,6,2))

        self.carList.append(Car(10,23,1,3,15,8,self.simulatorMap))
        self.simulatorMap[10][23].addCarID(1)
        self.carStatusBuff.append(carstatus(1,10,23))

        self.carList.append(Car(16,18,2,3,1,5,self.simulatorMap))
        self.simulatorMap[16][18].addCarID(2)
        self.carStatusBuff.append(carstatus(2,16,18))

        self.carList.append(Car(20,12,3,3,20,23,self.simulatorMap))
        self.simulatorMap[20][12].addCarID(3)
        self.carStatusBuff.append(carstatus(3,20,12))

    def printMap(self):
        os.system('clear')
        print ('')
        print ('---------------------------------')
        print ('cycle:',self.currentCycle)
        print ('---------------------------------')
        for i in range(self.mapSize):
            for j in range(self.mapSize):
                _carid = self.simulatorMap[i][j].getCarIDs()
                _lightid = self.simulatorMap[i][j].getLightID()
                if len(_carid)==1:
                    print ("<{0}>".format(_carid[0]).rjust(4), end="")
                elif len(_carid)>1:
                    print ("Boom".rjust(4),end="")
                    self.simulatorMap[i][j].clearRoadDirecs()
                    for c in _carid:
                        c.dealCrash()
                elif _lightid!=-1:
                    if self.lightList[_lightid].getSignal(self.currentCycle)==0:
                        print ("||".rjust(4), end="")
                    else:
                        print ("==".rjust(4), end="")
                elif self.simulatorMap[i][j].getRoadDirecNum()!=0:
                    print ("+".rjust(4), end="")
                else:
                    print (" ".rjust(4), end="")
            print ("")
    def printMapTest(self):
        print ('')
        print ('-----------------------')
        print ('cycle:',self.currentCycle)
        print ('-----------------------')
        for c in self.carList:
            print ("Car ",c.getDeviceID()," is at ","(",c.getPosX(),",",c.getPosY(),")")

    def checkCycleAndPosition(self,carid):
        myX = -1
        myY = -1
        #print ("In checkCycleAndPosition, carid is",carid)
        for s in self.carStatusBuff:
            if s.getStatusCarDevID()==carid:
                myX = s.getStatusCarPosX()
                myY = s.getStatusCarPosY()
                break
        if myX==-1 or myY==-1:
            print ("Invalid Car ID, return from check cycle and position.")
            return
        candp = []
        candp.append(self.currentCycle)
        candp.append(myX)
        candp.append(myY)
        return candp

    def lookAround(self,carid):
        myX = -1
        myY = -1
        for s in self.carStatusBuff:
            if s.getStatusCarDevID()==carid:
                myX = s.getStatusCarPosX()
                myY = s.getStatusCarPosY()
                break
        if myX==-1 or myY==-1:
            print ("Invalid Car ID, return from lookaround.")
            return
        tempStatusBuff = []
        tempDirec = self.simulatorMap[myX][myY].getRoadDirecs()
        for s in self.carStatusBuff:
            tempStatusX = s.getStatusCarPosX()
            tempStatusY = s.getStatusCarPosY()
            sr = self.carSightRange
            if tempDirec[0]==0:
                if tempStatusY>=myY-sr and tempStatusY<=myY+sr and tempStatusX>=myX-sr:
                    tempStatusBuff.append(s)
            elif tempDirec[0]==1:
                if tempStatusX>=myX-sr and tempStatusX<=myX+sr and tempStatusY<=myY+sr:
                    tempStatusBuff.append(s)
            elif tempDirec[0]==2:
                if tempStatusY>=myY-sr and tempStatusY<=myY+sr and tempStatusX<=myX+sr:
                    tempStatusBuff.append(s)
            elif tempDirec[0]==3:
                if tempStatusX>=myX-sr and tempStatusX<=myX+sr and tempStatusY>=myY-sr:
                    tempStatusBuff.append(s)
            else:
                print ("Error in looking around.")
        return tempStatusBuff

    def startSimulation(self):
        self.buildMap()
        self.createLights()
        self.createCars()
        while self.currentCycle<self.maxCycle:
            self.printMap()

            tempStatusList = []
            for c in self.carList:
                temps = c.carUpdate(self)
                tempStatusList.append(temps)
            self.carStatusBuff.clear()
            self.carStatusBuff = deepcopy(tempStatusList)

            for i in range(self.mapSize):
                for j in range(self.mapSize):
                    self.simulatorMap[i][j].clearCarIDs()
            for s in self.carStatusBuff:
                cx = s.getStatusCarPosX()
                cy = s.getStatusCarPosY()
                for c in self.carList:
                    if s.getStatusCarDevID()==c.getDeviceID():
                        if c.checkIfArrive()==0:
                            self.simulatorMap[cx][cy].addCarID(s.getStatusCarDevID())
                        break

            self.currentCycle+=1
            time.sleep(self.sleepInterval)





#end
