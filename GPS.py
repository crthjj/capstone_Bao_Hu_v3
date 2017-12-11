from copy import deepcopy
from Map import point

import playground, asyncio
from playground.network.packet.fieldtypes import UINT32, STRING, LIST, BUFFER

class GPSNetworkMessage(playground.network.packet.PacketType):
    DEFINITION_IDENTIFIER = "simulator.traffic.gps_message"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
    ("Timestamp", UINT32),
    ("Map", LIST(LIST(STRING))),
    ("Signature", BUFFER)

    ]

class GPSMessage():
    def __init__(self,cycle,m):
        self.GPSMessageCycle = cycle
        self.GPSMessageMap = deepcopy(m)
        self.signature = ""

class GPSListener(asyncio.Protocol):
    def __init__(self):
        self.unpacker = GPSNetworkMessage.Deserializer()
        self.GPSMsgQueue = []
    def data_received(self, data):
        self.unpacker.update(data)
        for pakcet in self.unpacker.nextPackets():
            m = GPSMessage(packet.Timestamp, packet.Map)
            self.GPSMsgQueue.append(m)
        return
    def receiveGPSMessageTest(self,m,c):
        if m.GPSMessageCycle!=c:
            return
        else:
            print ("receive one msg")
            self.GPSMsgQueue.append(m)

class GPSSender(asyncio.Protocol):
    def __init__(self):
        self.transport = None
    def connection_made(self, transport):
        self.transport = transport

    def sendGpsMessage(self, m):
        if not self.transport: raise Exception("Not yet connected!")
        networkMessage = GPSNetworkMessage(Timestamp=m.GPSMessageCycle, Map=m.GPSMessageMap, Signature=b"")
        self.transport.write(networkMessage.__serialize__())

class GPSServer():
    def __init__(self,s):
        self.__GPSMapSize = s
        self.__GPSCarList= []
        self.__GPSCarConnections = {}
        self.__GPSMap = [ [ "" for i in range(s)] for i in range(s) ]
        self.__GPSCurrentCycle = 0
    def constructGPSMap(self,pointmap):
        for i in range(self.__GPSMapSize):
            for j in range(self.__GPSMapSize):
                self.__GPSMap[i][j] = ""
                for direcs in pointmap[i][j].getRoadDirecs():
                    self.__GPSMap[i][j] += str(direcs)
    def GPSServerSendMessageTest(self):
        return GPSMessage(self.__GPSCurrentCycle,self.__GPSMap)
    def transmitCycle(self):
        # for each car in list
        # get address
    def getGPSCarlist(self):
        return self.__GPSCarList
    def addCarToList(self,carid, address, port):
        self.__GPSCarList.append(carid)
        c = playground.getConnector()
        c.create_playground_conenction(lambda: GPSSender(), address, port)
    def setGPSCycle(self,c):
        self.__GPSCurrentCycle = c
    def getGPSCycle(self):
        return self.__GPSCurrentCycle
