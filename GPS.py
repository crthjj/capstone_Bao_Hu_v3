from copy import deepcopy
from Map import point

import playground, asyncio, random, hashlib
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, LIST, BUFFER, STRING

GPS_BROADCAST_ADDRESS = "255.255.255.255"
SHARED_KEY = b"This is a shared key"

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
    def __init__(self,cs):
        print("Create GPSListener")
        self.unpacker = GPSNetworkMessage.Deserializer()
        self.GPSMsgQueue = []
        self.ifCheckSig = cs
    def connection_made(self, transport):
        print("{} Listener connected tp {}".format(transport.get_extra_info("hostname"), transport.get_extra_info("peername")))
        self.transport=transport
    def data_received(self, data):
        self.unpacker.update(data)
        for packet in self.unpacker.nextPackets():
            if self.ifCheckSig==0:
                m = GPSMessage(packet.Timestamp, packet.Map)
                self.GPSMsgQueue.append(m)
                continue
            sig = packet.Signature
            packet.Signature = b""
            checkSig = hashlib.sha256(packet.__serialize__()+SHARED_KEY).digest()
            if sig != checkSig:
                #print ("No Signature match. Ignoring")
                continue
            m = GPSMessage(packet.Timestamp, packet.Map)
            self.GPSMsgQueue.append(m)
        return
    def receiveGPSMessageTest(self,m,c):
        if m.GPSMessageCycle!=c:
            return
        else:
            #print ("receive one msg")
            self.GPSMsgQueue.append(m)

class GPSSender(asyncio.Protocol):
    def __init__(self):
        self.transport = None
    def connection_made(self, transport):
        self.transport = transport

    def sendGpsMessage(self, m, doSig):
        if not self.transport: raise Exception("Not yet connected!")
        networkMessage = GPSNetworkMessage(Timestamp=m.GPSMessageCycle, Map=m.GPSMessageMap, Signature=b"")
        if doSig:
            networkMessage.Signature = hashlib.sha256(networkMessage.__serialize__()+SHARED_KEY).digest()
        self.transport.write(networkMessage.__serialize__())

class GPSServer():
    def __init__(self,s):
        self.__GPSMapSize = s
        self.__GPSCarList= []
        self.__GPSCarConnections = {}
        self.__GPSMap = [ [ "" for i in range(s)] for i in range(s) ]
        self.__BadGPSMap = [ [ "" for i in range(s)] for i in range(s) ]
        self.__GPSCurrentCycle = 0
        self.__gpsSubscribers = {}
    def addGpsSubscriber(self, carId):
        txProtocol = GPSSender()
        self.__gpsSubscribers[carId] = txProtocol
        return txProtocol
    def constructGPSMap(self,pointmap):
        for i in range(self.__GPSMapSize):
            for j in range(self.__GPSMapSize):
                self.__GPSMap[i][j] = ""
                self.__BadGPSMap[i][j] = ""
                direcs = pointmap[i][j].getRoadDirecs()
                self.__GPSMap[i][j] = "".join([str(d) for d in direcs])
    def GPSServerSendMessageTest(self):
        return GPSMessage(self.__GPSCurrentCycle,self.__GPSMap)
    def GPSServerSendConfusingMessageTest(self):
        return GPSMessage(self.__GPSCurrentCycle, self.__BadGPSMap)
    def transmitCycle(self):
        # for each car in list
        # get address
        gpsMessage = self.GPSServerSendMessageTest()
        badGpsMessage = self.GPSServerSendConfusingMessageTest()
        for carId in self.__GPSCarList:
            if not carId in self.__gpsSubscribers:
                continue
            #print("send gps message to car ID {}".format(carId))
            self.__gpsSubscribers[carId].sendGpsMessage(gpsMessage, doSig=True)
            self.__gpsSubscribers[carId].sendGpsMessage(badGpsMessage, doSig=False)
    def getGPSCarlist(self):
        return self.__GPSCarList
    def addCarToList(self,carid):
        self.__GPSCarList.append(carid)
        c = playground.getConnector()
        coro = c.create_playground_connection(lambda: self.addGpsSubscriber(carid), GPS_BROADCAST_ADDRESS, 100+carid)
        asyncio.get_event_loop().create_task(coro)
    def setGPSCycle(self,c):
        self.__GPSCurrentCycle = c
        self.transmitCycle()
    def getGPSCycle(self):
        return self.__GPSCurrentCycle
