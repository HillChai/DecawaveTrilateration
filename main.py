from dataAnalysis import processor
import numpy as np
import os
from ctypes import *

CUR_PATH = os.path.dirname(__file__)  # 获取当前运行脚本的绝对路径
dllPath = os.path.join(CUR_PATH, "trilateration.dll")
pDll = cdll.LoadLibrary(dllPath)


class UWBMsg(Structure):
    _fields_ = [("x", c_double),
                ("y", c_double),
                ("z", c_double)]

def trilateration(anchorPos, distances):
# def trilateration():

    location = UWBMsg()
    anchorArray = (UWBMsg * 8)()
    distanceArray = (c_int * 8)(-1)

    for i in range(4):
        anchorArray[i].x = anchorPos[i][0]
        anchorArray[i].y = anchorPos[i][1]
        anchorArray[i].z = anchorPos[i][2]
        distanceArray[i] = distances[i]

    # 无效的测距值一定给 -1，否则会用随机数进行运算
    distanceArray[4] = -1
    distanceArray[5] = -1
    distanceArray[6] = -1
    distanceArray[7] = -1

    result = pDll.GetLocation(byref(location), anchorArray, distanceArray)
    return location.x, location.y, location.z

# anchorPos = [[0,0,0], [0.95,0,0], [0, 1.87, 0], [0.95, 1.87, 0]]
# distances = [2990, 3180, 2960, 2870]
# print(trilateration(anchorPos, distances))

# walkPosition = [np.array([1.2, 0.49, 2.6 + (0.8 - 2.6) * i / 427]) for i in range(427)]

# MARK: Step 0 Check no.

# MARK: Step 1 UWB position
path = "./rawData/"
anchorPos = [[0,0,0], [0.95,0,0], [0, 1.87, 0], [0.95, 1.87, 0]]
target = processor(path=path, jsonName="6-16-40-10", anchorPos=anchorPos)
target.getBLEmessage()
distances = target.getDistancesFromBLEmessage()

dllPositions = []
for i in range(target.n):
    x,y,z = trilateration(anchorPos, [int(distances[i][j] * 1000) for j in range(4)])
    dllPositions.append([x,y,z])

print(dllPositions)
target.Position2D(dllPositions, "dllPositions")

uwbResults = target.calculateByDecawave(distances)
target.Position2D(uwbResults, "uwbResults")
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
