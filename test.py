#!/usr/bin/python3
import time
from Map import point
from trafficSimulator import trafficSimulator
import os, asyncio

mapsize = 25
maxcycle = 50
sleepinterval = 2
'''
trafficMap = [ [ point() for i in range(mapsize)] for i in range(mapsize) ]
for i in range(mapsize):
    for j in range(mapsize):
        trafficMap[i][j].setCordinate(i,j)

for i in range(mapsize):
    trafficMap[i][1].addRoadDirecs(2)
for i in range(mapsize):
    trafficMap[i][3].addRoadDirecs(0)
for j in range(mapsize):
    trafficMap[2][j].addRoadDirecs(1)
for j in range(mapsize):
    trafficMap[3][j].addRoadDirecs(1)

print (trafficMap[0][1].getRoadDirecs())
#def __init__(self,x,y,devid,maxv,destx,desty,trafficmap)
car0 = car(0,1,0,3,0,3,trafficMap)
'''

s = trafficSimulator(mapsize,maxcycle,sleepinterval)

from playground.common.logging import EnablePresetLogging, PRESET_DEBUG
EnablePresetLogging(PRESET_DEBUG)
asyncio.get_event_loop().call_soon(s.startSimulation)
asyncio.get_event_loop().run_forever()
