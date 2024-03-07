from dataAnalysis import processor
import numpy as np
import os
from ctypes import *
import _ctypes
import ctypes


class UWBMsg(Structure):
    _fields_ = [("x", c_double),
                ("y", c_double),
                ("z", c_double)]

location = UWBMsg()
anchorArray = (UWBMsg*4)()
distanceArray = (c_int*4)(-1)


CUR_PATH=os.path.dirname(__file__)
dllPath=os.path.join(CUR_PATH, "trilateration.dll")
pDll=cdll.LoadLibrary(dllPath)
result=0

path = "./rawData/"
anchorPos = [[0,0,0], [0.95,0,0], [0, 1.87, 0], [0.95, 1.87, 0]]

for i in range(4):
    anchorArray[i].x = anchorPos[i][0]
    anchorArray[i].y = anchorPos[i][1]
    anchorArray[i].z = anchorPos[i][2]

walkPosition = [np.array([1.2, 0.49, 2.6 + (0.8 - 2.6) * i / 427]) for i in range(427)]

target = processor(path=path, jsonName="6-16-40-10",anchorPos=anchorPos)

# MARK: Step 0 Check no.

# MARK: Step 1 UWB position
target.getBLEmessage()
distances = target.getDistancesFromBLEmessage()

dllResults = []

for i in range(len(distances)):
    result = pDll.Getlocation(byref(location), anchorArray, distanceArray)
    dllResults.append([location.x, location.y, location.z])
print("dllResults: ", len(dllResults))

uwbResults = target.calculateByDecawave(distances)
# target.Position3D(uwbResults, "UWB", xlimInterval = [-1,1], ylimInterval=[1,2], zlimInterval=[-3,0])
# backDistances = target.backCheckUWBResults(uwbResults)
# target.draw4DistanceComparingGraphs(distances=distances, unknowDistances=backDistances)
# target.draw4DistanceDifferenceGraphs(distances, backDistances)

# MARK: Step 2 ARKit position
# target.getPosition()
# ARKitPosition = target.position
# target.Position3D(ARKitPosition, "ARKit", xlimInterval = [-1,1], ylimInterval=[-0.6,0.6], zlimInterval=[-2,2])
# MARK: Step 3 distance compare

# MARK: Step 3.1 distances
