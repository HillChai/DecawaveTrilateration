from math import sqrt

class threeDimensionalLocation:
    def __init__(self):
        self.bestSolution = [0]*3

    def leastSquaresMethod(self, anchorPos: list, distances: list) -> int:
        # Matrix * pos^T = b^T
        noValidDistances = 0

        for d in distances:
            if d > 0:
                noValidDistances += 1

        if noValidDistances < 3:
            return -1  # UWB_ANC_BELOW_THREE

        anchorsOnXYPlane = True  # 是否在同一XY平面，是
        for i in range(1, noValidDistances):
            if anchorPos[i][2] != anchorPos[0][2]:
                anchorsOnXYPlane = False  # 是否在同一XY平面，否
                break

        '''
         check the matrix
         | x1 - x0  x2 - x0 |
         | y1 - y0  y2 - y0 | has rank 2
         '''
        linearDependent = True
        i = 2  # num of vectors which are linear independent
        while linearDependent and i < noValidDistances:

            crossItem1 = (anchorPos[i][1] - anchorPos[0][1]) * \
                         (anchorPos[1][0] - anchorPos[0][0])  # (y2 - y0)*(x1 - x0)
            crossItem2 = (anchorPos[1][1] - anchorPos[0][1]) * \
                         (anchorPos[i][0] - anchorPos[0][0])  # (y1 - y0)*(x2 - x0)
            if (crossItem1 - crossItem2) != 0:
                linearDependent = False
                break
            i += 1

        if linearDependent:
            return -2  # UWB_LIN_DEP_FOR_THREE

        '''
        If the anchors are not on the same plane, three vectors must be independent
        '''
        if not anchorsOnXYPlane:
            if noValidDistances < 4:
                return -3  # UWB_ANC_ON_ONE_LEVEL
            '''
            Check if the matrix
            |x1 - x0 x2 - x0 x3 - x0|
            |y1 - y0 y2 - y0 y3 - y0|  has rank 3, (rank 2 is already satisfied)
            |z1 - z0 z2 - z0 z3 - z0|
            '''

            linearDependent = True
            j = 2
            while linearDependent and i < noValidDistances:
                if j != i:
                    # (x1 - x0)*[(y2 - y0)*(zj - z0) - (yj - y0)*(z2 - z0)]
                    temp = (anchorPos[2][1] - anchorPos[0][1]) * (anchorPos[j][2] - anchorPos[0][2]) - \
                           (anchorPos[j][1] - anchorPos[0][1]) * (anchorPos[2][2] - anchorPos[0][2])
                    temp2 = (anchorPos[1][0] - anchorPos[0][0]) * temp
                    # + (x2 - x0)*[(yj - y0)*(z1 - z0) - (y1 - y0)*(zj - z0)]
                    temp = (anchorPos[j][1] - anchorPos[0][1]) * (anchorPos[1][2] - anchorPos[0][2]) - \
                           (anchorPos[1][1] - anchorPos[0][1]) * (anchorPos[j][2] - anchorPos[0][2])
                    temp2 += (anchorPos[2][0] - anchorPos[0][0]) * temp
                    # + (xj - x0)*[(y1 - y0)*(z2 - z0) - (y2 - y0)*(z1 - z0)]
                    temp = (anchorPos[1][1] - anchorPos[0][1]) * (anchorPos[2][2] - anchorPos[0][2]) - \
                           (anchorPos[2][1] - anchorPos[0][1]) * (anchorPos[1][2] - anchorPos[0][2])
                    temp2 += (anchorPos[j][0] - anchorPos[0][0]) * temp

                    if temp2 != 0:
                        linearDependent = False
                j += 1

            if linearDependent:
                return -4  # UWB_LIN_DEP_FOR_FOUR

        M11, M12, M13, M22, M23, M33 = 0, 0, 0, 0, 0, 0
        b0, b1, b2 = 0, 0, 0
        for k in range(1, noValidDistances):
            M11 += (anchorPos[k][0] - anchorPos[0][0]) ** 2
            M12 += (anchorPos[i][0] - anchorPos[0][0]) * (anchorPos[i][1] - anchorPos[0][1])
            M13 += (anchorPos[i][0] - anchorPos[0][0]) * (anchorPos[i][2] - anchorPos[0][2])
            M22 += (anchorPos[i][1] - anchorPos[0][1]) ** 2
            M23 += (anchorPos[i][1] - anchorPos[0][1]) * (anchorPos[i][2] - anchorPos[0][2])
            M33 += (anchorPos[i][2] - anchorPos[0][2]) ** 2

            temp = distances[0] ** 2 - distances[i] ** 2 + anchorPos[i][0] ** 2 + anchorPos[i][1] ** 2 + \
                   anchorPos[i][2] ** 2 - anchorPos[0][0] ** 2 - anchorPos[0][1] ** 2 - anchorPos[0][2] ** 2
            b0 += (anchorPos[k][0] - anchorPos[0][0]) * temp
            b1 += (anchorPos[k][1] - anchorPos[k][1]) * temp
            b2 += (anchorPos[k][2] - anchorPos[k][2]) * temp

        M11 = 2 * M11
        M12 = 2 * M12
        M13 = 2 * M13
        M22 = 2 * M22
        M23 = 2 * M23
        M33 = 2 * M33

        x_pos, y_pos, z_pos = 0, 0, 0
        if not anchorsOnXYPlane:
            '''
            If the anchors are not in the same x-y plane,
                |M11 M12 b0|
                |M12 M22 b1|
                |M13 M23 b2|
            z = -------------
                |M11 M12 M13|
                |M12 M22 M23|
                |M13 M23 M33|
            '''
            numinator = b0 * (M12 * M23 - M13 * M22) + b1 * (M12 * M13 - M11 * M23) + b2 * \
                        (M11 * M22 - M12 * M12)
            denominator = M13 * (M12 * M23 - M13 * M22) + M23 * (M12 * M13 - M11 * M23) + M33 * \
                          (M11 * M22 - M12 * M12)

            if denominator == 0:
                return -5  # UWB_RANK_ZERO

            z_pos = ((numinator * 10) / denominator + 5) / 10  # cm精度下，四入五入
        else:
            z_pos = 0  # z_pos calculated after x_pos and y_pos

        '''
        |M11 M12| |x|   |b0 - M13*z|
        |       | | | = |          |
        |M12 M22| |y|   |b1 - M23*z|

             |M11  b0-M13*z|
             |M12  b1-M23*z|
        y = ------------------
               |M11   M12|
               |M12   M22|
        '''
        numinator = b1 * M11 - b0 * M12 - (z_pos * (M11 * M23 - M12 * M13))
        denominator = M11 * M22 - M12 * M12

        if not denominator:
            return -5  # UWB_RANK_ZERO

        y_pos = ((numinator * 10) / denominator + 5) / 10

        '''
        [M11 M12 M13] [x y z]^T = [b0 b1 b2]^T

        x = b0 - z * M13 - y * M12
        '''
        numinator = b0 - z_pos * M13 - y_pos * M12
        denominator = M11

        x_pos = ((numinator * 10) / denominator + 5) / 10

        '''
        z^2 = meanDistance^2 - (x - xk)^2 - (y - yk)^2
        '''
        if anchorsOnXYPlane:
            for k in range(noValidDistances):
                temp = distances[k] ** 2 - (x_pos - anchorPos[k][0]) ** 2 \
                       - (y_pos - anchorPos[k][1]) ** 2
                if temp >= 0:
                    z_pos += sqrt(temp)
                else:
                    z_pos += 0
            z_pos = z_pos / noValidDistances

        self.bestSolution[0] = x_pos
        self.bestSolution[1] = y_pos
        self.bestSolution[2] = z_pos

        return 1  # UWB_OK


# anchorPos = [[0,0,15], [53.7,0,15], [0,78,15], [53.7,78,15]]
# distances = [84, 102, 80, 87]
# method = threeDimensionalLocation()
# method.leastSquaresMethod(anchorPos, distances)
# print(method.bestSolution)

