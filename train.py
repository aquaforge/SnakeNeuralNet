from datetime import datetime
import json
from random import randint
import numpy as np
from Brains.BrainSimpleNN import BrainSimpleNN
from DbSnakeData import DbSnakeData
from DbTrainData import DbTrainData
from Enums.MoveDirection import MoveDirection


def dtNow():
    return datetime.now().strftime("%H:%M:%S")


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

if len(trainData) > 0:
    print(dtNow(), "data loaded")
    dbo = DbSnakeData()
    for i in range(500):
        viewRadius, td = trainData[randint(0, len(trainData)-1)]
        b = BrainSimpleNN.getNewTrainedBrain(viewRadius, td)
        if b._mse < 0.12:
            info = b._model.info()
            info["mse"] = b._mse
            info["viewRadius"] = b._viewRadius
            dbo.saveNN(info)
        print(dtNow(), i, viewRadius, b._mse)

print(dtNow(), "done")
