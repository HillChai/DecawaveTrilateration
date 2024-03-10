from dataAnalysis import processor
import numpy as np

# anchorPos = [[0,0,0], [0.95,0,0], [0, 1.87, 0], [0.95, 1.87, 0]]
# distances = [2990, 3180, 2960, 2870]
# print(trilateration(anchorPos, distances))

# walkPosition = [np.array([1.2, 0.49, 2.6 + (0.8 - 2.6) * i / 427]) for i in range(427)]

# MARK: Step 0 Check no.

# MARK: Step 1 UWB position

anchorPos1 = [[0,0,0], [0.95,0,0], [0, 1.87, 0], [0.95, 1.87, 0]]  #A0在竖墙左下, A1在左上，A2在右下
anchorPos2 = [[0,0,0], [1.05,0,0], [0, 1.81, 0], [1.05, 1.81, 0]]  #A0在竖墙右下, A1在右上，A2在左下
anchorPos3 = [[0,0,1.8], [1.81,0,1.8], [0, 3.2 ,1.8], [1.81, 3.2, 1.8]]  #A0在横墙窗角
path = "./rawData/anchorPos3/"
target = processor(path=path, jsonName="9-12-1-46", anchorPos=anchorPos3)
target.getBLEmessage()
distances = target.getDistancesFromBLEmessage()

'''
ARKit
'''
target.getPosition()
ARKitPosition = target.position
# target.Position2D(ARKitPosition, "ARKit")
target.Position3D(ARKitPosition, "ARKit")

'''
单点比较打印
'''
# i = 40 + 150
# x,y,z = target.trilaterationInDll([int(distances[i][j] * 1000) for j in range(4)])
# print("dll:", x, y, z)
# x,y,z = target.calculateOneByDecawave(distances[i], 2)
# print("mine:", x,y,z)

'''

整体比较图
 '''
dllPositions = []
for i in range(len(distances)):
    x,y,z = target.trilaterationInDll([int(distances[i][j] * 1000) for j in range(4)])
    dllPositions.append([x,y,z])
uwbResults = target.calculateByDecawave(distances,2)
target.Position2DTogether(dllPositions, uwbResults, "Red Dll and Blue mine")

# target.Position2D(dllPositions, "dllPositions")
target.Position3D(dllPositions, "dll")


# target.Position2D(uwbResults, "uwbResults")
target.Position3D(uwbResults, "UWB")
# backDistances = target.backCheckUWBResults(uwbResults)
# target.draw4DistanceComparingGraphs(distances=distances, unknowDistances=backDistances)
# target.draw4DistanceDifferenceGraphs(distances, backDistances)

# MARK: Step 2 ARKit position
# target.getPosition()
# ARKitPosition = target.position
# target.Position2D(ARKitPosition, "ARKit")
# target.Position3D(ARKitPosition, "ARKit")
# MARK: Step 3 distance compare
# target.Position2DTogether(ARKitPosition, uwbResults, "Red ARKit and Blue UWB")

# MARK: Step 3.1 distances
