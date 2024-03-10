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

    def draw2D(self,title):
        f, ax = plt.subplots(2,2)
        f.suptitle(title)

        ax[0][0].plot([i for i in range(self.n)], self.x)
        # plt.ylim(-0.5, 1)
        ax[0][0].set_title("X-axis")

        ax[0][1].plot([i for i in range(self.n)], self.y)
        # plt.ylim(-0.5, 1)
        ax[0][1].set_title("Y-axis")

        ax[1][0].plot([i for i in range(self.n)], self.z)
        # plt.ylim(-0.5, 1)
        # ax[1][0].set_title("Z-axis")

        plt.show()


    def draw3D(self, title):
        ax4 = plt.subplot(projection="3d")
        ax4.set_title(title)
        ax4.scatter(self.x[:self.n//2], self.y[:self.n//2], self.z[:self.n//2], c='r')
        ax4.scatter(self.x[self.n // 2:], self.y[self.n // 2:], self.z[self.n // 2:], c='b')
        ax4.set_xlabel('X')
        ax4.set_xlim([-0.5,2])
        ax4.set_ylabel('Y')
        ax4.set_ylim([-0.5,2])
        ax4.set_zlabel('Z')
        ax4.set_zlim([-0.5,2])
        plt.show()

