from datetime import datetime
import json
from random import randint
import numpy as np
from Brains.BrainSimpleNN import BrainSimpleNN
from DbSnakeData import DbSnakeData
from DbTrainData import DbTrainData
from Enums.MoveDirection import MoveDirection

infoList = list()


def dtNow():
    return datetime.now().strftime("%H:%M:%S")

def save():
    global infoList

    if len(infoList) > 0:
        dbo = DbSnakeData()
        for info in infoList:
            dbo.saveNN(info)
        dbo = None
        infoList = list()
        print(dtNow(), "saved")


dbo = DbTrainData()
distinctRadius = dbo.getDistinctViewRadius()
if len(distinctRadius) == 0:
    print(dtNow(), "no data")
else:
    trainData = list()
    for i in distinctRadius:
        td = (dbo.getTrainData(i, 20000),
              dbo.getTrainData(i, 1000))
        if td[0][0] is not None:
            trainData.append((i, td))
        print(dtNow(), "data", i)
dbo = None

if len(trainData) > 0:
    print(dtNow(), "data loaded")
    for i in range(5000):
        viewRadius, td = trainData[randint(0, len(trainData)-1)]
        b = BrainSimpleNN.getNewTrainedBrain(viewRadius, td)
        print(dtNow(), i, viewRadius, b._mse)
        if b._mse < 0.12:
            info = b._model.info()
            info["mse"] = b._mse
            info["viewRadius"] = b._viewRadius
            infoList.append(info)
            if len(infoList) > 20:
                save()

save(infoList)
print(dtNow(), "done")
