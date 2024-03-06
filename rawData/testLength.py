import json
import matplotlib.pyplot as plt

path = "moveForward10cm.json"
with open (path, encoding="utf-8") as f:
    data = json.load(f)
    position = []
    n = len(data)
    x, y, z = [], [], []

    for i in range(n):
        position.append(data[i]["position"])
        x.append(data[i]["position"][0])
        y.append(data[i]["position"][1])
        z.append(data[i]["position"][2])

    fig = plt.figure()
    # ax1 = fig.add_subplot(2, 2, 1)
    # ax1.plot([i for i in range(n)], x)
    # plt.ylabel("x")
    # ax2 = fig.add_subplot(2, 2, 2)
    # ax2.plot([i for i in range(n)], y)
    # plt.ylabel("y")
    # ax3 = fig.add_subplot(2, 2, 3)
    # ax3.plot([i for i in range(n)], z)
    # plt.ylabel("z")
    ax4 = plt.subplot(projection = "3d")
    ax4.scatter(x,y,z,c = 'r')
    ax4.set_xlabel('X')
    ax4.set_ylabel('Y')
    ax4.set_zlabel('Z')
    plt.show()