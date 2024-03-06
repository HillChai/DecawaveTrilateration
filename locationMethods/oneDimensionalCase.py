from math import sqrt

class oneDimensionalLocation:
    def __init__(self):
        self.bestSolution = [0]*3

    def findPointA(self, x1: float, y1: float, x2: float, y2: float, d1: float, d2: float):

        d = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        fabsD = abs(d1 - d2)
        delta = 0
        if d1 + d2 < d or fabsD > d:
            delta = d - d2 - d1
            if delta >= 0:
                d1 += delta / 2
                d2 += delta / 2
            else:
                delta = (abs(d1 - d2) - d) / 2
                symbol = -1 if d1 > d2 else 1
                d1 += delta * symbol
                d2 -= delta * symbol

        a = (d1 ** 2 - d2 ** 2 + d ** 2) / (2 * d)
        h = sqrt(abs(d1 ** 2 - a ** 2))

        x3 = x1 + a * (x2 - x1) / d
        y3 = y1 + a * (y2 - y1) / d

        x4 = x3 + h * (y2 - y1) / d
        y4 = y3 - h * (x2 - x1) / d

        x5 = x3 - h * (y2 - y1) / d
        y5 = y3 + h * (x2 - x1) / d

        if h == 0:
            self.bestSolution[0] = x3
            self.bestSolution[1] = y3
        else:
            xi = (x4 + x5) / 2
            yi = (y4 + y5) / 2
            self.bestSolution[0] = xi
            self.bestSolution[1] = yi



# x1 = 1
# y1 = 1
# x2 = 2
# y2 = 2
# d1 = 2.828
# d2 = 1.414
# method = oneDimensionalLocation()
# method.findPointA(x1,y1,x2,y2,d1,d2)
# print(method.bestSolution)