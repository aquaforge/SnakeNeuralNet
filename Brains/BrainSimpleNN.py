from random import randint, random
import numpy as np
from Brains.BrainBase import BrainBase
from Enums.MoveDirection import MoveDirection
from SimpleNN import ActivationRelu, Layer, SimpleNN


class BrainSimpleNN (BrainBase):
    def __init__(self, viewRadius: int, model: SimpleNN, numTrainings: int, mse:float):
        super().__init__(viewRadius)
        self._model = model
        self._numTrainings = numTrainings
        self._mse = mse

    def getDirection(self, input_vector: np.array) -> MoveDirection:
        output_vector = self._model.predict(input_vector.T)
        return MoveDirection(output_vector.argmax())

    @staticmethod
    def getNewTrainedBrain(viewRadius: int, trainData: tuple):
        (x_train, y_train), (x_test, y_test) = trainData

        size = (2*viewRadius+1)**2

        l = list()
        l.append(Layer(nodesCount=size))
        l.append(Layer(nodesCount=size//2, activationClass=ActivationRelu, useBias=True))
        l.append(Layer(nodesCount=len(MoveDirection),activationClass=ActivationRelu, useBias=True))
        model = SimpleNN(layers=l, learningRate=0.01)

        if x_train is None or y_train is None:
            return BrainSimpleNN(viewRadius, model, 0)

        numTrainings = randint(30000, 120000)
        for _ in range(numTrainings):
            k = randint(0,x_train.shape[0]-1)
            model.train(x_train[k,:,:], y_train[k,:])

        pred = np.empty(shape=y_test.shape)
        for i in range(y_test.shape[0]):
            pred[i,:] = model.predict(x_test[i,:,:]).reshape(pred.shape[1])

        mse = SimpleNN.mseLoss(y_test, pred)

        return BrainSimpleNN(viewRadius, model, numTrainings, mse)
