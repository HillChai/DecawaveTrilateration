import numpy as np
from math import sqrt

def deca3DLocate (solution1: list, solution2: list, bestSolution: list,\
                  noOfSolution: int, best3DError: float, bestGdopRate):

    return


'''
3 TRIL_3PHERES, and return two solutions: result1, result2
4 TRIL_4PHERES, and return one solution: bestSolution

Errors if negative number is returned
MAXZERO: machine epsilon 0.001
'''

bestSolution = np.zeros([0,0,0])
result1, result2 = np.array([0,0,0]), np.array([0,0,0])
def trilateration(anchorPos, distances, maxzero: float):
    #Three spheres, and need to consider concentric spheres
    global bestSolution
    global result1, result2
    p1, p2, p3, p4 = np.array(anchorPos[0]), np.array(anchorPos[1]), np.array(anchorPos[2]), np.array(anchorPos[3])
    r1, r2, r3, r4 = distances[0], distances[1], distances[2], distances[3]

    ex = p3 - p1
    h = np.linalg.norm(ex)

    if h <= maxzero:
        return -1 # ERR_TRIL_CONCENTRIC

    ex = p3 - p2
    h = np.linalg.norm(ex)
    if h <= maxzero:
        return -1

    ####################################################################
    ex = p2 - p1
    h = np.linalg.norm(ex)
    if h <= maxzero:
        return -1

    ex = ex / h  # New unit vectot from p1 towards p2.

    t1 = p3 - p1
    i = np.dot(ex, t1)
    t2 = ex*i
    ey = t1 - t2
    t = np.linalg.norm(ey)
    if t > maxzero:
        ey /= t
        j = np.dot(ey, t1)
    else:
        j = 0.0

    # print("j:", j)
    if abs(j) <= maxzero:   #p3 is on the line of p1p2
        '''
        In the case that three centres are on one line, there is only one possible solution
        which means the three spheres are tangent on one point. Otherwise, it is impossible
        for the sphere 3 to get the circle intersected from sphere 1 and sphere 2.
        '''
        t2 = p1 + ex*r1
        if abs(np.linalg.norm(p2 - t2) - r2) <= maxzero and abs(np.linalg.norm(p3 - t2) - r3) <= maxzero:
            '''
            Three centres are in one line, and p2 - t2 = r2*ex, t2 - p1 = r1*ex, mean the tangent
            point of two circles are on the line. t2 is the only solution.
            '''
            result1 = t2
            result2 = t2
            return 3  # TRIL_3SPHERES

        '''
        Consider the other direction of the line if t2 above doesn't satisfy.
        '''
        t2 = p1 + ex * (-r1)
        if abs(np.linalg.norm(p2 - t2) - r2) <= maxzero and abs(np.linalg.norm(p3 - t2) - r3) <= maxzero:
            result1 = t2
            result2 = t2
            return 3 # TRIL_3SPHERES

        return -2 # ERR_TRIL_COLINEAR_2SOLUTIONS

    ez = np.cross(ex, ey)
    x = (r1**2 - r2**2) / (2*h) + h / 2  # law of cosines
    y = (r1**2 - r3**2 + i**2) / (2*j) + j/2 - x*i/j   # (x, y) * (i, j)
    z = r1**2 - x**2 - y**2
    if z < -maxzero:
        return -3 # ERR_TRIL_SQRTNEGNUMB
    elif z > 0.0:
            z = sqrt(z)
    else:
        z = 0.0

    t2 = p1 + ex*x
    t2 = t2 + ey*y

    result1 = t2 + ez*z
    result2 = t2 - ez*z

    print(result1, result2)
    '''
    Two points from the first three spheres.
    '''
    #######################################################################
    '''
    One point if one more sphere
    If sphere 4 is is concentric to one of them, then it is no use.
    '''

    ex = p4 - p1
    h = np.linalg.norm(ex)
    if h <= maxzero:
        return 3  # TRIL_3SPHERES

    ex = p4 - p2
    h = np.linalg.norm(ex)
    if h <= maxzero:
        return 3  # TRIL_3SPHERES

    ex = p4 - p3
    h = np.linalg.norm(ex)
    if h <= maxzero:
        return 3  # TRIL_3SPHERES

    t3 = result1 - p4
    i = np.linalg.norm(t3)
    t3 = result2 - p4
    h = np.linalg.norm(t3)

    if i > h:
        bestSolution = result1
        result1 = result2
        result2 = bestSolution

    cnt4 = 0
    rr4 = r4
    result = 1
    mu1, mu2, mu = 0.0, 0.0, 0.0

    def sphereline(p1: np.ndarray, p2: np.ndarray, sc: np.ndarray, r: float):
        global mu1, mu2
        '''
        :param p1, p2: line
        :param sc: sphere circle
        :param r: radius
        :param mu1, mu2: constants
        :return zero if successful
        '''
        dp = p2 - p1

        a = np.sum(dp ** 2)
        b = 2 * np.sum(dp * (p1 - sc))
        c = np.sum(sc ** 2 + p1 ** 2 - 2 * sc * p1) - r ** 2

        bb4ac = b ** 2 - 4 * a * c

        if abs(a) == 0 or bb4ac < 0:
            mu1 = 0
            mu2 = 0
            return 1

        mu1 = (-b + sqrt(bb4ac)) / (2 * a)
        mu2 = (-b - sqrt(bb4ac)) / (2 * a)

        return 0

    while result and cnt4 < 10:
        print(1)
        result = sphereline(result1, result2, p4, rr4)
        rr4 += 0.1
        cnt4 += 1

    if result:
        bestSolution = result1   #迭代最多10次后取最近的作为答案
    else:
        if mu1 < 0 and mu2 < 0:
            if abs(mu1) <= abs(mu2):
                mu = mu1
            else:
                mu = mu2

            ex = result2 - result1
            h = np.linalg.norm(ex)
            ex = ex / h
            mu = 0.5*mu
            t2 = ex*mu*h
            bestSolution = t2

        elif mu1 < 0 and mu2 > 1 or mu2 < 0 and mu1 > 1:
            if mu1 > mu2:
                mu = mu1
            else:
                mu = mu2
            ex = result2 - result1
            h = np.linalg.norm(ex)
            ex = ex / h
            t2 = ex * mu*h
            t2 = t2 + result1
            t3 = (result2 - t2)*0.5
            bestSolution = t2 + t3

        elif (mu1 > 0 and mu1 < 1) and (mu2 < 0 or mu2 > 1) or \
                (mu2 > 0 and mu2 < 1) and (mu1 < 0 or mu1 > 1):
            if mu1 >= 0 and mu1 <= 1:
                mu = mu1
            else:
                mu = mu2
            if mu <= 0.5:
                mu -= 0.5*mu
            else:
                mu -= 0.5*(1-mu)
            ex = result2 - result1
            h = np.linalg.norm(ex)
            ex /= h
            t2 = ex*mu*h
            t2 = result1 + t2
            bestSolution = t2

        elif mu1 == mu2:
            mu = mu1
            if mu <= 0.25:
                mu -= 0.5*(mu)
            elif mu <= 0.5:
                mu -= 0.5*(0.5-mu)
            elif mu <= 0.75:
                mu -= 0.5*(mu-0.5)
            else:
                mu -= 0.5*(1-mu)
            ex = result2 - result1
            h = np.linalg.norm(ex)
            t2 = ex*mu*h
            t2 = result1 + t2
            bestSolution = t2

        else:
            '''
            Middlepoint
            '''
            mu = mu1 + mu2
            ex = result2 - result1
            h = np.linalg.norm(ex)
            ex /= h
            mu = 0.5*mu
            t2 = ex * mu*h
            t2 = result1 + t2
            bestSolution = t2

    return 4 # TRIL_4SPHERES



anchorPos = [[0,0,0], [3,0,0],[2,0,0],[0,0,0]]
distances = [1,2,1,1]
maxzero = 0.001
result = trilateration(anchorPos, distances, maxzero)
print(result)
print("result1, result2:", result1, result2)
