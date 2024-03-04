from threeDimensionalCase import threeDimensionalLocation
from twoDimensionalCase import twoDimensionalLocation
from oneDimensionalCase import oneDimensionalLocation

class generalLocation:

    def __init__(self):
        self.bestSolution = [0]*3

    def GetLocation(self, anchorPos: list, distances: list, dimensional: int):
        validAnchors = []
        noOfValidAnchor = 0
        use3Anchors = 0  # Whether you use 3 anchors.

        for i in range(4):
            if distances[i] > 0:
                validAnchors.append([anchorPos[i][0], anchorPos[i][1], anchorPos[i][2], distances[i]])
                noOfValidAnchor += 1

        if dimensional == 3:
            method = threeDimensionalLocation()
            result = method.leastSquaresMethod(anchorPos, distances)
            self.bestSolution = method.bestSolution
            return result

        elif dimensional == 1:
            if noOfValidAnchor < 2:
                return -1
            else:
                sortedDistances = sorted(distances)
                index1 = distances.index(sortedDistances[1])
                index2 = distances.index(sortedDistances[2])
                method = oneDimensionalLocation()
                method.findPointA(anchorPos[index1][0], anchorPos[index1][1],anchorPos[index2][0],
                                  anchorPos[index2][1], distances[index1], distances[index2])
                self.bestSolution = method.bestSolution
                return 1

        elif dimensional == 2:
            if noOfValidAnchor < 3:
                return -1
            elif noOfValidAnchor == 3:
                use3Anchors = 1

            method = twoDimensionalLocation(anchorPos, distances)
            result = method.deca3DLocate()

            if result >= 0:
                if method.result1[2] <= method.result2[2]:
                    self.bestSolution[2] = method.result1[2]
                else:
                    self.bestSolution[2] = method.result2[2]
                if use3Anchors == 1 or result == 3:
                    p1 = method.p1
                    if method.result1 < p1[2]:
                        self.bestSolution = method.result1
                    else:
                        self.bestSolution = method.result2
                return result

            return -1

        else:
            return -1
