from threeDimensionalCase import leastSquaresMethod
from twoDimensionalCase import deca3DLocate
from oneDimensionalCase import findPointA

def GetLocation(bestSolution: list, anchorPos: list, distances: list, dimensional: int):

    validAnchors = []
    noOfValidAnchor = 0
    bestSolution = [0]*3
    use3Anchors = 0  # Whether use 3 anchors.

    for i in range(4):
        if distances[i] > 0:
            validAnchors.append([anchorPos[i][0], anchorPos[i][1], anchorPos[i][2], distances[i]])
            noOfValidAnchor += 1

    if dimensional == 3:
        result = leastSquaresMethod(bestSolution, anchorPos, distances)
        return result

    elif dimensional == 1:
        if noOfValidAnchor < 2:
            return -1
        else:
            sortedDistances = sorted(distances)
            index1 = distances.index(sortedDistances[1])
            index2 = distances.index(sortedDistances[2])
            findPointA(bestSolution, anchorPos[index1][0], anchorPos[index1][1],\
                       anchorPos[index2][0], anchorPos[index2][1], distances[index1], distances[index2])
            return 1

    elif dimensional == 2:
        if noOfValidAnchor < 3:
            return -1
        elif noOfValidAnchor == 3:
            use3Anchors = 1

        result = deca3DLocate()




