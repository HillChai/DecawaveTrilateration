import numpy as np
from math import sqrt


class twoDimensionalLocation:

    def __init__(self, anchorPos: list, distances: list):
        self.p1 = np.array(anchorPos[0])
        self.p2 = np.array(anchorPos[1])
        self.p3 = np.array(anchorPos[2])
        self.p4 = np.array(anchorPos[3])
        self.r1 = distances[0]
        self.r2 = distances[1]
        self.r3 = distances[2]
        self.r4 = distances[3]
        self.bestSolution = np.zeros(3)
        self.result1, self.result2 = np.zeros(3), np.zeros(3)
        self.mu1, self.mu2 = 0.0, 0.0
        self.maxzero = 0.001
        self.best_3derror = 0
        self.best_gdoprate = 1
        self.nosolution_count = 0 #failed attempts count
        self.combination = 0

    '''
        Update mu1, mu2
        :param p1, p2: line
        :param sc: sphere circle
        :param r: radius
        :param mu1, mu2: constants
        :return zero if successful
    '''

    def sphereline(self, sc, r):
        dp = self.p2 - self.p1

        a = np.sum(dp ** 2)
        b = 2 * np.sum(dp * (self.p1 - sc))
        c = np.sum(sc ** 2 + self.p1 ** 2 - 2 * sc * self.p1) - r ** 2

        bb4ac = b ** 2 - 4 * a * c

        if abs(a) == 0 or bb4ac < 0:
            self.mu1 = 0
            self.mu2 = 0
            return -1

        self.mu1 = (-b + sqrt(bb4ac)) / (2 * a)
        self.mu2 = (-b - sqrt(bb4ac)) / (2 * a)

        return 0

    '''
    3spheres: return 3, update result1 result2
    4spheres: return 4, update bestSolution
    '''

    def trilateration(self):
        # Three spheres, and need to consider concentric spheres
        ex = self.p3 - self.p1
        h = np.linalg.norm(ex)

        if h <= self.maxzero:
            return -1  # ERR_TRIL_CONCENTRIC

        ex = self.p3 - self.p2
        h = np.linalg.norm(ex)
        if h <= self.maxzero:
            return -1

        ####################################################################
        ex = self.p2 - self.p1
        h = np.linalg.norm(ex)
        if h <= self.maxzero:
            return -1

        ex = ex / h  # New unit vectot from p1 towards p2.

        t1 = self.p3 - self.p1
        i = np.dot(ex, t1)
        t2 = ex * i
        ey = t1 - t2
        t = np.linalg.norm(ey)
        if t > self.maxzero:
            ey /= t
            j = np.dot(ey, t1)
        else:
            j = 0.0

        # print("j:", j)
        if abs(j) <= self.maxzero:  # p3 is on the line of p1p2
            '''
            In the case that three centres are on one line, there is only one possible solution
            which means the three spheres are tangent on one point. Otherwise, it is impossible
            for the sphere 3 to get the circle intersected from sphere 1 and sphere 2.
            '''
            t2 = self.p1 + ex * self.r1
            if abs(np.linalg.norm(self.p2 - t2) - self.r2) <= self.maxzero and abs(
                    np.linalg.norm(self.p3 - t2) - self.r3) <= self.maxzero:
                '''
                Three centres are in one line, and p2 - t2 = r2*ex, t2 - p1 = r1*ex, mean the tangent
                point of two circles are on the line. t2 is the only solution.
                '''
                self.result1 = t2
                self.result2 = t2
                return 3  # TRIL_3SPHERES

            '''
            Consider the other direction of the line if t2 above doesn't satisfy.
            '''
            t2 = self.p1 + ex * (-self.r1)
            if abs(np.linalg.norm(self.p2 - t2) - self.r2) <= self.maxzero and abs(
                    np.linalg.norm(self.p3 - t2) - self.r3) <= self.maxzero:
                self.result1 = t2
                self.result2 = t2
                return 3  # TRIL_3SPHERES

            return -2  # ERR_TRIL_COLINEAR_2SOLUTIONS

        ez = np.cross(ex, ey)
        x = (self.r1 ** 2 - self.r2 ** 2) / (2 * h) + h / 2  # law of cosines
        y = (self.r1 ** 2 - self.r3 ** 2 + i ** 2) / (2 * j) + j / 2 - x * i / j  # (x, y) * (i, j)
        z = self.r1 ** 2 - x ** 2 - y ** 2
        if z < -self.maxzero:
            return -3  # ERR_TRIL_SQRTNEGNUMB
        elif z > 0.0:
            z = sqrt(z)
        else:
            z = 0.0

        t2 = self.p1 + ex * x
        t2 = t2 + ey * y

        self.result1 = t2 + ez * z
        self.result2 = t2 - ez * z

        # print(self.result1, self.result2)
        '''
        Two points from the first three spheres.
        '''
        #######################################################################
        '''
        One point if one more sphere
        If sphere 4 is is concentric to one of them, then it is no use.
        '''

        ex = self.p4 - self.p1
        h = np.linalg.norm(ex)
        if h <= self.maxzero:
            return 3  # TRIL_3SPHERES

        ex = self.p4 - self.p2
        h = np.linalg.norm(ex)
        if h <= self.maxzero:
            return 3  # TRIL_3SPHERES

        ex = self.p4 - self.p3
        h = np.linalg.norm(ex)
        if h <= self.maxzero:
            return 3  # TRIL_3SPHERES

        t3 = self.result1 - self.p4
        i = np.linalg.norm(t3)
        t3 = self.result2 - self.p4
        h = np.linalg.norm(t3)

        '''
        closer
        '''
        if i > h:
            self.bestSolution = self.result1
            self.result1 = self.result2
            self.result2 = self.bestSolution

        cnt4 = 0
        rr4 = self.r4
        result = 1

        while result and cnt4 < 10:
            # print(1)
            result = self.sphereline(self.p4, rr4)
            rr4 += 0.1
            cnt4 += 1

        if result:
            self.bestSolution = self.result1  # 迭代最多10次后取最近的作为答案
        else:
            if self.mu1 < 0 and self.mu2 < 0:
                if abs(self.mu1) <= abs(self.mu2):
                    mu = self.mu1
                else:
                    mu = self.mu2

                ex = self.result2 - self.result1
                h = np.linalg.norm(ex)
                ex = ex / h
                mu = 0.5 * mu
                t2 = ex * mu * h
                self.bestSolution = t2

            elif self.mu1 < 0 and self.mu2 > 1 or self.mu2 < 0 and self.mu1 > 1:
                if self.mu1 > self.mu2:
                    mu = self.mu1
                else:
                    mu = self.mu2
                ex = self.result2 - self.result1
                h = np.linalg.norm(ex)
                ex = ex / h
                t2 = ex * mu * h
                t2 = t2 + self.result1
                t3 = (self.result2 - t2) * 0.5
                self.bestSolution = t2 + t3

            elif (self.mu1 > 0 and self.mu1 < 1) and (self.mu2 < 0 or self.mu2 > 1) or \
                    (self.mu2 > 0 and self.mu2 < 1) and (self.mu1 < 0 or self.mu1 > 1):
                if self.mu1 >= 0 and self.mu1 <= 1:
                    mu = self.mu1
                else:
                    mu = self.mu2
                if mu <= 0.5:
                    mu -= 0.5 * mu
                else:
                    mu -= 0.5 * (1 - mu)
                ex = self.result2 - self.result1
                h = np.linalg.norm(ex)
                ex /= h
                t2 = ex * mu * h
                t2 = self.result1 + t2
                self.bestSolution = t2

            elif self.mu1 == self.mu2:
                mu = self.mu1
                if mu <= 0.25:
                    mu -= 0.5 * (mu)
                elif mu <= 0.5:
                    mu -= 0.5 * (0.5 - mu)
                elif mu <= 0.75:
                    mu -= 0.5 * (mu - 0.5)
                else:
                    mu -= 0.5 * (1 - mu)
                ex = self.result2 - self.result1
                h = np.linalg.norm(ex)
                t2 = ex * mu * h
                t2 = self.result1 + t2
                self.bestSolution = t2

            else:
                '''
                Middlepoint
                '''
                mu = self.mu1 + self.mu2
                ex = self.result2 - self.result1
                h = np.linalg.norm(ex)
                ex /= h
                mu = 0.5 * mu
                t2 = ex * mu * h
                t2 = self.result1 + t2
                self.bestSolution = t2

        return 4

    def gdoprate(self):
        ex = self.p1 - self.bestSolution
        h = np.linalg.norm(ex)
        t1 = ex / h

        ex = self.p2 - self.bestSolution
        h = np.linalg.norm(ex)
        t2 = ex / h

        ex = self.p3 - self.bestSolution
        h = np.linalg.norm(ex)
        t3 = ex / h

        gdop1 = abs(np.dot(t1, t2))
        gdop2 = abs(np.dot(t2, t3))
        gdop3 = abs(np.dot(t3, t1))

        result = max(gdop1, gdop2, gdop3)
        return result

    def deca3DLocate(self):
        trilateration_errcounter = 0
        trilateration_mode34 = 0
        combination_counter = 4
        gdoprate_compare2 = 1

        while combination_counter:
            success = 0
            result = 0
            concentric = 0
            overlook_count = 0
            ovr_r1, ovr_r2, ovr_r3, ovr_r4 = self.r1, self.r2, self.r3, self.r4

            # CM_ERR_ADDED 5,10
            while not success and overlook_count <= 10 and not concentric:
                result = self.trilateration()

                if result == 3:
                    trilateration_mode34 = 3
                    success = 1
                elif result == 4:
                    trilateration_mode34 = 4
                    success = 1
                elif result == -1:
                    concentric = 1
                else:
                    ovr_r1 += 0.1
                    ovr_r2 += 0.1
                    ovr_r3 += 0.1
                    ovr_r4 += 0.1
                    overlook_count += 1

            if success:
                if result == 3:
                    self.nosolution_count = overlook_count
                    combination_counter = 0
                elif result == 4:
                    gdoprate_compare1 = self.gdoprate()
                    if gdoprate_compare1 <= gdoprate_compare2:
                        self.nosolution_count = overlook_count
                        self.best_3derror = sqrt((np.linalg.norm(self.bestSolution - self.p1) - self.r1) ** 2 + \
                                            (np.linalg.norm(self.bestSolution - self.p2) - self.r2) ** 2 + \
                                            (np.linalg.norm(self.bestSolution - self.p3) - self.r3) ** 2 + \
                                            (np.linalg.norm(self.bestSolution - self.p4) - self.r4) ** 2)
                        self.best_gdoprate = gdoprate_compare1
                        gdoprate_compare2 = gdoprate_compare1
                    self.combination = 5 - combination_counter
                    ptemp = self.p1
                    self.p1 = self.p2
                    self.p2 = self.p3
                    self.p3 = self.p4
                    self.p4 = ptemp

                    rtemp = self.r1
                    self.r1 = self.r2
                    self.r2 = self.r3
                    self.r3 = self.r4
                    self.r4 = rtemp

                    combination_counter -= 1
            else:
                trilateration_errcounter += 1
                combination_counter -= 1

        if trilateration_errcounter >= 4:
            return -1
        else:
            return trilateration_mode34



# anchorPos = [[0,0,0], [3,0,0],[2,0,0],[0,0,0]]   # concentric case
# distances = [1,2,1,1]
# anchorPos = [[0, 0, 0], [2, 0, 0], [0, -2, 0], [0.25, -0.25, 2 * 2]]
# distances = [1, 2, 2, 0.935]
# method = twoDimensionalLocation([0,0,0], anchorPos, distances)
# method.trilateration()
# print(method.bestSolution, method.result1, method.result2)