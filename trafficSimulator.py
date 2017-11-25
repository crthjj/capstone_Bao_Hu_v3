#!/usr/bin/python3
from Map import point,carmessage
from Device import Car,Light
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
        self.carMessageBuf = []
        self.simulatorMap = [ [ point() for i in range(msize)] for i in range(msize) ]

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

        self.carList.append(Car(10,23,1,3,15,8,self.simulatorMap))
        self.simulatorMap[10][23].addCarID(1)

        self.carList.append(Car(16,18,2,3,1,5,self.simulatorMap))
        self.simulatorMap[16][18].addCarID(2)

        self.carList.append(Car(20,12,3,3,20,23,self.simulatorMap))
        self.simulatorMap[20][12].addCarID(3)

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
    def startSimulation(self):
        self.buildMap()
        self.createLights()
        self.createCars()
        while self.currentCycle<self.maxCycle:
            self.printMap()
            self.carMessageBuf.clear()
            for c in self.carList:
                self.carMessageBuf.append(c.sendMsg())
            for c in self.carList:
                tempMsgBuff = []
                tempDirec = self.simulatorMap[c.getPosX()][c.getPosY()].getRoadDirecs()
                for msg in self.carMessageBuf:
                    tempMsgX = msg.getMsgCarPosX()
                    tempMsgY = msg.getMsgCarPosY()
                    mv = c.getMaxVelocity()
                    if tempDirec[0]==0:
                        if tempMsgY>=c.getPosY()-mv and tempMsgY<=c.getPosY()+mv and tempMsgX>=c.getPosX()-mv:
                            tempMsgBuff.append(msg)
                    elif tempDirec[0]==1:
                        if tempMsgX>=c.getPosX()-mv and tempMsgX<=c.getPosX()+mv and tempMsgY<=c.getPosY()+mv:
                            tempMsgBuff.append(msg)
                    elif tempDirec[0]==2:
                        if tempMsgY>=c.getPosY()-mv and tempMsgY<=c.getPosY()+mv and tempMsgX<=c.getPosX()+mv:
                            tempMsgBuff.append(msg)
                    elif tempDirec[0]==3:
                        if tempMsgX>=c.getPosX()-mv and tempMsgX<=c.getPosX()+mv and tempMsgY>=c.getPosY()-mv:
                            tempMsgBuff.append(msg)
                    else:
                        print ("Error in receiving message.")
                c.receiveMsg(tempMsgBuff,self.currentCycle)
            for i in range(self.mapSize):
                for j in range(self.mapSize):
                    self.simulatorMap[i][j].clearCarIDs()
            for c in self.carList:
                if c.checkIfArrive()==0:
                    self.simulatorMap[c.getPosX()][c.getPosY()].addCarID(c.getDeviceID())

            self.currentCycle+=1
            time.sleep(self.sleepInterval)





#end
