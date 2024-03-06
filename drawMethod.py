import matplotlib.pyplot as plt

class painter:
    def __init__(self, position):
        self.n = len(position)
        self.x = []
        self.y = []
        self.z = []
        for i in range(self.n):
            self.x.append(position[i][0])
            self.y.append(position[i][1])
            self.z.append(position[i][2])

    def draw2D(self):
        fig = plt.figure()
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.plot([i for i in range(self.n)], self.x)
        plt.ylabel("x")
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.plot([i for i in range(self.n)], self.y)
        plt.ylabel("y")
        ax3 = fig.add_subplot(2, 2, 3)
        ax3.plot([i for i in range(self.n)], self.z)
        plt.ylabel("z")
        plt.show()

    def draw3D(self):
        ax4 = plt.subplot(projection="3d")
        ax4.scatter(self.x, self.y, self.z, c='r')
        ax4.set_xlabel('X')
        ax4.set_ylabel('Y')
        ax4.set_zlabel('Z')
        plt.show()

