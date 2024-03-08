import json
import os
from matplotlib import pyplot as plt

from locationMethods import generalLocation
from drawMethod import painter
import numpy as np

class processor:
    def __init__(self, path, jsonName, anchorPos):
        self.anchorPos = anchorPos
        self.walkPosition = []
        self.IdealDistances = []
        self.data = []
        self.n = 0
        self.id = []
        self.position = []
        self.eulerAngle = []
        self.BLEmessage = []
        with open (path + jsonName + ".json", encoding="utf-8") as f:
            # content = f.read()
            # a = json.loads(content)    #字符串转python任何类型，此处为列表
            self.data = json.load(f)
            self.n = len(self.data)
    def getPosition(self):
        for i in range(self.n):
            self.position.append(self.data[i]["position"])

    def geteulerAngle(self):
        for i in range(self.n):
            self.eulerAngle.append(self.data[i]["eulerAngle"])

    def getID(self):
        for i in range(self.n):
            self.id.append(self.data[i]["id"])

    def getBLEmessage(self):
        for i in range(self.n):
            self.BLEmessage.append(self.data[i]["BLEmessage"])

    def checkNoPhoto(self):
        cnt_success = 0
        for name in self.id:
            if os.access(self.path + name + ".jpg", os.F_OK):  # F_OK, R_OK, W_OK, X_OK
                cnt_success += 1
        print("cnt_total, cnt_success: ", self.n, cnt_success)

    def getDistancesFromBLEmessage(self) -> list:
        distances = []
        for i in range(self.n):
            strs = self.BLEmessage[i].split("$")
            # print(strs[1])
            strs = strs[0].split(" ")

            d = []
            for s in strs[2:6]:
                value = 0
                for i in range(8):
                    value += int(s[7 - i], 16) * (16 ** i)
                d.append(value / 1000)
                # d.append(value)
            distances.append(d)
        return distances

    def calculateOneByDecawave(self, distances, dimensional) -> list:
        method = generalLocation()
        result = method.GetLocation(anchorPos=self.anchorPos, distances=distances,dimensional=dimensional)
        return method.bestSolution



    def calculateByDecawave(self, distances, dimensional) -> list:
        method = generalLocation()
        uwbResults = []
        for i in range(self.n):
            result = method.GetLocation(anchorPos=self.anchorPos, distances=distances[i],dimensional=dimensional)
            # print("result symbol: ", result)
            uwbResults.append(method.bestSolution)
        return uwbResults

    def backCheckUWBResults(self, uwbResults):
        backDistances = []
        for i in range(self.n):
            l1 = np.linalg.norm(uwbResults[i] - self.anchorPos[0])
            l2 = np.linalg.norm(uwbResults[i] - self.anchorPos[1])
            l3 = np.linalg.norm(uwbResults[i] - self.anchorPos[2])
            l4 = np.linalg.norm(uwbResults[i] - self.anchorPos[3])
            backDistances.append([l1, l2, l3, l4])
        return backDistances
    def calculateByARKit(self) -> list:
        return self.position

    def setIdealTrack(self, walkPosition):
        self.walkPosition = walkPosition
        for i in range(self.n):
            l1 = np.linalg.norm(walkPosition[i] - self.anchorPos[0])
            l2 = np.linalg.norm(walkPosition[i] - self.anchorPos[1])
            l3 = np.linalg.norm(walkPosition[i] - self.anchorPos[2])
            l4 = np.linalg.norm(walkPosition[i] - self.anchorPos[3])
            self.walkDistances.append([l1, l2, l3, l4])

    def Position2D(self, pos, title):
        person = painter(pos)
        person.draw2D(title)

    def Position2DTogether(self, pos1, pos2, title):
        if len(pos1) != len(pos2):
            print("len(pos1) != len(pos2)")
            return

        n = len(pos1)
        f, ax = plt.subplots(2, 2)
        f.suptitle(title)

        ax[0][0].plot([i for i in range(n)], [pos1[i][0] for i in range(n)], c='r')
        ax[0][0].plot([i for i in range(n)], [pos2[i][0] for i in range(n)], c='b')
        # plt.ylim(-0.5, 1)
        ax[0][0].set_title("X-axis")

        ax[0][1].plot([i for i in range(n)], [pos1[i][1] for i in range(n)], c='r')
        ax[0][1].plot([i for i in range(n)], [pos2[i][1] for i in range(n)], c='b')
        # plt.ylim(-0.5, 1)
        ax[0][1].set_title("Y-axis")

        ax[1][0].plot([i for i in range(n)], [pos1[i][2] for i in range(n)], c='r')
        ax[1][0].plot([i for i in range(n)], [pos2[i][2] for i in range(n)], c='b')
        # plt.ylim(-0.5, 1)
        # ax[1][0].set_title("Z-axis")

        plt.show()

    def Position3D(self, pos, title, xlimInterval, ylimInterval, zlimInterval):
        person = painter(pos)
        person.draw3D(title, xlimInterval, ylimInterval, zlimInterval)

    def draw4DistanceComparingGraphs(self, distances, unknowDistances):
        print(len(distances), len(unknowDistances))
        fig = plt.figure()
        #A0
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.plot([i for i in range(self.n)], [distances[i][0] for i in range(self.n)], c='r')
        ax1.plot([i for i in range(self.n)], [unknowDistances[i][0] for i in range(self.n)], c='b')
        # plt.ylim(-0.5, 1)
        plt.ylabel("A0")
        # A1
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.plot([i for i in range(self.n)], [distances[i][1] for i in range(self.n)], c='r')
        ax2.plot([i for i in range(self.n)], [unknowDistances[i][1] for i in range(self.n)], c='b')
        # plt.ylim(-0.5, 1)
        plt.ylabel("A1")
        # A2
        ax3 = fig.add_subplot(2, 2, 3)
        ax3.plot([i for i in range(self.n)], [distances[i][2] for i in range(self.n)], c='r')
        ax3.plot([i for i in range(self.n)], [unknowDistances[i][2] for i in range(self.n)], c='b')
        plt.ylabel("A2")
        # A3
        ax4 = fig.add_subplot(2, 2, 4)
        ax4.plot([i for i in range(self.n)], [distances[i][3] for i in range(self.n)], c='r')
        ax4.plot([i for i in range(self.n)], [unknowDistances[i][3] for i in range(self.n)], c='b')
        # plt.ylim(-0.5, 1)
        plt.ylabel("A3")
        plt.show()

    def draw4DistanceDifferenceGraphs(self, distances, unknowDistances):
        fig = plt.figure()
        # A0
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.plot([i for i in range(self.n)], [distances[i][0] - unknowDistances[i][0] for i in range(self.n)], c='g')
        plt.ylabel("A0")
        # A1
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.plot([i for i in range(self.n)], [distances[i][1] - unknowDistances[i][1] for i in range(self.n)], c='g')
        plt.ylabel("A1")
        # A2
        ax3 = fig.add_subplot(2, 2, 3)
        ax3.plot([i for i in range(self.n)], [distances[i][2] - unknowDistances[i][2] for i in range(self.n)], c='g')
        plt.ylabel("A2")
        # A3
        ax4 = fig.add_subplot(2, 2, 4)
        ax4.plot([i for i in range(self.n)], [distances[i][3] - unknowDistances[i][3] for i in range(self.n)], c='g')
        plt.ylabel("A3")
        plt.show()






