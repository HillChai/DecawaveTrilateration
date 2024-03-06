import json
import os
from locationMethods import generalLocation
from drawMethod import painter

path = "rawData/28-12-31-31/"

def checkNum(id:list, path:str):
    cnt_success = 0
    for name in id:
        if os.access(path + name + ".jpg", os.F_OK):  # F_OK, R_OK, W_OK, X_OK
            cnt_success += 1
    print("cnt_total: ", len(a))
    print("cnt_success: ", cnt_success)

def transform16into10(BLEmessage:list) -> list:
    distances = []
    for i in range(n):
        strs = BLEmessage[i].split("$")
        # print(strs[1])
        strs = strs[0].split(" ")

        d = []
        for s in strs[2:6]:
            value = 0
            for i in range(8):
                value += int(s[7-i], 16)*(16**i)
            d.append(value/1000)
        distances.append(d)
    return distances

with open (path + "28-12-31-31.json", encoding="utf-8") as f:
    # content = f.read()=
    # a = json.loads(content)    #字符串转python任何类型，此处为列表
    a = json.load(f)
    # print("a:", type(a))
    # print("a[0]:", a[0])
    id = []
    position = []
    eulerAngle = []
    BLEmessage = []
    n = len(a)


    for i in range(n):
        id.append(a[i]["id"])
        position.append(a[i]["position"])
        eulerAngle.append(a[i]["eulerAngle"])
        BLEmessage.append(a[i]["BLEmessage"])

    # MARK: Step 1  whether the data collect is the same as no. of photos
    checkNum(id, path)
    # MARK: Step 2  get the distances among tag and anchors
    distances = transform16into10(BLEmessage)
    # MARK: Step 3  calculate with Decawave methods
    method = generalLocation()
    anchorPos = [[0,0,0.15], [0.537,0,0.15], [0, 0.78, 0.15], [0.537, 0.78, 0.15]]
    result = method.GetLocation(anchorPos, distances[0], 2)
    print("result: ", result)
    print("bestSolution: ", method.bestSolution)
    # MARK: Step 4 draw
    person = painter(position)
    person.draw2D()
    # person.draw3D()


