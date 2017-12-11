#!/usr/bin/python3
from Map import point,carstatus,carmovement
from Device import Car,Light,Badcar,GPSCar
from copy import deepcopy
from GPS import GPSMessage,GPSServer,GPSListener
import time
import os

class trafficSimulator():
    def __init__(self,msize,maxc,sleepInt):
        self.currentCycle = 0
        self.maxCycle = maxc
        self.mapSize = msize
        self.sleepInterval = sleepInt
        self.deviceList = []
        self.lightList = []
        self.deviceStatusList = []
        self.tempStatusList = []
        self.simulatorMap = [ [ point() for i in range(msize)] for i in range(msize) ]
        self.carSightRange = 3
        self.simuGPSServer = GPSServer(self.mapSize)

        for i in range(msize):
            for j in range(msize):
                self.simulatorMap[i][j].setCordinate(i,j)

    def buildMap(self):
        '''
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
        '''
        self.addRoad(3,1,3,4,1)
        self.addRoad(3,2,14,2,0)
        self.addRoad(8,0,8,4,1)
        self.addRoad(5,4,8,4,0)
        self.addRoad(5,1,5,4,3)
        self.addRoad(11,1,11,4,1)
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
                    self.lightList.append(Light(i,j,lightnum,4,self.simulatorMap))
    def createCars(self):
        #def __init__(self,x,y,devid,maxv,destx,desty,trafficmap):
        '''
        self.deviceList.append(Car(6,2,0,3,11,27,self.simulatorMap))
        self.simulatorMap[6][2].addCarID(0)
        self.deviceStatusList.append(carstatus(0,6,2))

        self.deviceList.append(Car(10,23,1,3,15,8,self.simulatorMap))
        self.simulatorMap[10][23].addCarID(1)
        self.deviceStatusList.append(carstatus(1,10,23))

        self.deviceList.append(Car(16,18,2,3,1,5,self.simulatorMap))
        self.simulatorMap[16][18].addCarID(2)
        self.deviceStatusList.append(carstatus(2,16,18))

        self.deviceList.append(Car(20,12,3,3,20,23,self.simulatorMap))
        self.simulatorMap[20][12].addCarID(3)
        self.deviceStatusList.append(carstatus(3,20,12))
        '''
        self.deviceList.append(GPSCar(13,2,0,3,3,4,self.simulatorMap))
        self.simulatorMap[13][2].addCarID(0)
        self.deviceStatusList.append(carstatus(0,13,2))

        self.deviceList.append(Car(14,2,1,3,3,3,self.simulatorMap))
        self.simulatorMap[14][2].addCarID(1)
        self.deviceStatusList.append(carstatus(1,14,2))

    def createCarsTest(self):
        self.deviceList.append(Car(6,2,0,3,11,27,self.simulatorMap))
        self.simulatorMap[6][2].addCarID(0)
        self.deviceStatusList.append(carstatus(0,6,2))

        self.deviceList.append(Badcar(4,2,1,3,11,27,self.simulatorMap))
        self.simulatorMap[4][2].addCarID(1)
        self.deviceStatusList.append(carstatus(1,4,2))

        self.deviceList.append(Car(16,18,2,3,1,5,self.simulatorMap))
        self.simulatorMap[16][18].addCarID(2)
        self.deviceStatusList.append(carstatus(2,16,18))

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
                    print ("B{0},{1}".format(_carid[0],_carid[1]).rjust(4),end="")
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
        for c in self.deviceList:
            print ("Car ",c.getDeviceID()," is at ","(",c.getPosX(),",",c.getPosY(),")")

    def checkCycleAndPosition(self,carid):
        myX = -1
        myY = -1
        #print ("In checkCycleAndPosition, carid is",carid)
        for s in self.deviceStatusList:
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
        for s in self.deviceStatusList:
            if s.getStatusCarDevID()==carid:
                myX = s.getStatusCarPosX()
                myY = s.getStatusCarPosY()
                break
        if myX==-1 or myY==-1:
            print ("Invalid Car ID, return from lookaround.")
            return
        tempStatusBuff = []
        tempDirec = self.simulatorMap[myX][myY].getRoadDirecs()
        if len(tempDirec)==0:
            return []
        for s in self.deviceStatusList:
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
    def clearDeviceOnMap(self):
        for i in range(self.mapSize):
            for j in range(self.mapSize):
                self.simulatorMap[i][j].clearCarIDs()
        self.tempStatusList.clear()
    def updateStatusList(self):
        self.deviceStatusList.clear()
        self.deviceStatusList = deepcopy(self.tempStatusList)
    def crashDevice(self,crashid):
        for d in self.deviceList:
            if d.getDeviceID()==crashid:
                d.dealCrash()
                break
    def feedGPSMessage(self,devid):
        print ("Feed GPSMSG to device {0}".format(devid))
        return self.simuGPSServer.GPSServerSendMessageTest()
    def applyMovement(self,movement,device):
        if movement is None:
            return

        stepList = movement.getMovement()
        devID = movement.getMovementCarID()
        curX = -1
        curY = -1
        for s in self.deviceStatusList:
            if devID==s.getStatusCarDevID():
                curX = s.getStatusCarPosX()
                curY = s.getStatusCarPosY()
                break
        if curX==-1 or curY==-1:
            print ("Apply movement fail, no such device.")
            return
        moveX = curX
        moveY = curY
        for s in stepList:
            #print ("step is:",s)
            if s==0:
                if len(self.simulatorMap[moveX-1][moveY].getRoadDirecs())==0:
                    print ("Device {0} movement illegal.".format(devID))
                    break
                else:
                    moveX = moveX-1
                    if len(self.simulatorMap[moveX][moveY].getCarIDs())>0:
                        self.simulatorMap[moveX][moveY].clearRoadDirecs()
                        device.dealCrash()
                        for ids in self.simulatorMap[moveX][moveY].getCarIDs():
                            print ("in simulator, crash device ",ids)
                            self.crashDevice(ids)
                        break
            elif s==1:
                if len(self.simulatorMap[moveX][moveY+1].getRoadDirecs())==0:
                    print ("Device {0} movement illegal.".format(devID))
                    break
                else:
                    moveY = moveY+1
                    if len(self.simulatorMap[moveX][moveY].getCarIDs())>0:
                        self.simulatorMap[moveX][moveY].clearRoadDirecs()
                        device.dealCrash()
                        for ids in self.simulatorMap[moveX][moveY].getCarIDs():
                            print ("in simulator, crash device ",ids)
                            self.crashDevice(ids)
                        break
            elif s==2:
                if len(self.simulatorMap[moveX+1][moveY].getRoadDirecs())==0:
                    print ("Device {0} movement illegal.".format(devID))
                    break
                else:
                    moveX = moveX+1
                    if len(self.simulatorMap[moveX][moveY].getCarIDs())>0:
                        self.simulatorMap[moveX][moveY].clearRoadDirecs()
                        device.dealCrash()
                        for ids in self.simulatorMap[moveX][moveY].getCarIDs():
                            print ("in simulator, crash device ",ids)
                            self.crashDevice(ids)
                        break
            elif s==3:
                if len(self.simulatorMap[moveX][moveY-1].getRoadDirecs())==0:
                    print ("Device {0} movement illegal.".format(devID))
                    break
                else:
                    moveY = moveY-1
                    if len(self.simulatorMap[moveX][moveY].getCarIDs())>0:
                        self.simulatorMap[moveX][moveY].clearRoadDirecs()
                        device.dealCrash()
                        for ids in self.simulatorMap[moveX][moveY].getCarIDs():
                            print ("in simulator, crash device ",ids)
                            self.crashDevice(ids)
                        break
            else:
                print ("Illegal movement")
                break
        if moveX==device.getDestPosX() and moveY==device.getDestPosY():
            device.dealArrive()
            print ("Device {0} has arrived.".format(devID))
        else:
            self.simulatorMap[moveX][moveY].addCarID(devID)
            self.tempStatusList.append(carstatus(devID,moveX,moveY))

    def startSimulation(self):
        self.buildMap()
        self.createLights()
        #self.createCars()
        self.createCars()
        while self.currentCycle<self.maxCycle:
            self.printMap()

            self.clearDeviceOnMap()
            if self.currentCycle==2:
                self.simulatorMap[6][2].clearRoadDirecs()
            #self.deviceStatusList is for this cycle
            #send GPS message here
            self.simuGPSServer.setGPSCycle(self.currentCycle)
            self.simuGPSServer.constructGPSMap(self.simulatorMap)
            for d in self.deviceList:
                #print ("device {0} updating".format(d.getDeviceID()))
                tempMovement = d.Update(self)
                self.applyMovement(tempMovement,d)

            self.updateStatusList()

            self.currentCycle+=1
            time.sleep(self.sleepInterval)





#end
