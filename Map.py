
class point():

    def __init__(self):
        self.__posX = 0
        self.__posY = 0
        self.__lightID = -1
        self.__carIDs = []
        self.__roadDirecs = []
        self.__pointLightRule = -1

    def getPosX(self):
        return self.__posX
    def getPosY(self):
        return self.__posY
    def getCarIDs(self):
        ids = self.__carIDs.copy()
        return ids
    def getLightID(self):
        return self.__lightID
    def getPointLightRule(self):
        return self.__pointLightRule
    def getRoadDirecNum(self):
        return len(self.__roadDirecs)
    def getRoadDirecs(self):
        return self.__roadDirecs
    def clearCarIDs(self):
        self.__carIDs.clear()
    def addCarID(self,carid):
        self.__carIDs.append(carid)
    def setLightID(self,lightnum):
        self.__lightID = lightnum
    def setPointLightRule(self,rule):
        self.__pointLightRule = rule
    def setCordinate(self,x,y):
        self.__posX = x
        self.__posY = y
    def addRoadDirecs(self,direc):
        self.__roadDirecs.append(direc)
    def clearRoadDirecs(self):
        self.__roadDirecs.clear()

class carstatus():

    def __init__(self,carid,carx,cary):
        self.__carID = carid
        self.__carX = carx
        self.__carY = cary

    def getStatusCarDevID(self):
        return self.__carID
    def getStatusCarPosX(self):
        return self.__carX
    def getStatusCarPosY(self):
        return self.__carY

#end
