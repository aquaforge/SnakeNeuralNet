from random import randint, random
import numpy as np
from Brains.BrainBase import BrainBase
from Enums.MoveDirection import MoveDirection
from SimpleNN import ActivationRelu, Layer, SimpleNN


class BrainSimpleNN (BrainBase):
    def __init__(self, viewRadius: int, model: SimpleNN, mse: float = 0):
        super().__init__(viewRadius)
        self._model = model
        self._mse = mse

    def getDirection(self, input_vector: np.array) -> MoveDirection:
        output_vector = self._model.predict(
            BrainSimpleNN.prepareInputVector(input_vector.T))
        return MoveDirection(output_vector.argmax())

    @staticmethod
    def getNewTrainedBrain(viewRadius: int, trainData: tuple):
        (x_train, y_train), (x_test, y_test) = trainData

        size = 2*(2*viewRadius+1)**2

        l = list()
        l.append(Layer(nodesCount=size))
        l.append(Layer(nodesCount=int(size/1.5),
                 activationClass=ActivationRelu, useBias=True))
        # if random() > 0.5:
        #     l.append(Layer(nodesCount=int(size/(2.6+random())),
        #              activationClass=ActivationRelu, useBias=random() > 0.5))
        l.append(Layer(nodesCount=len(MoveDirection),
                 activationClass=ActivationRelu, useBias=True))
        model = SimpleNN(layers=l, learningRate=0.01)

        if x_train is None or y_train is None:
            return BrainSimpleNN(viewRadius, model, 0)

        numTrainings = randint(2000, 50000)
        for _ in range(numTrainings):
            k = randint(0, x_train.shape[0]-1)
            model.train(BrainSimpleNN.prepareInputVector(
                x_train[k, :, :]), y_train[k, :])
            pass

        pred = np.empty(shape=y_test.shape)
        for i in range(y_test.shape[0]):
            pred[i, :] = model.predict(BrainSimpleNN.prepareInputVector(x_test[i, :, :])).reshape(pred.shape[1])

        mse = SimpleNN.mseLoss(y_test, pred)

        return BrainSimpleNN(viewRadius, model, mse)

    @staticmethod
    def prepareInputVector(inputVector):
        # print("-----")
        # print(inputVector)
        e = np.array(inputVector).copy()
        e[e == -3] = 0
        e[e == -2] = 0
        e[e == -1] = 0
        # print(e)

        w = np.array(inputVector).copy()
        w[w == 1] = 0
        w[w == -3] = -1
        w[w == -2] = -1
        # print(w)

        return 0.999 * np.concatenate((e.flatten(), w.flatten())).astype(np.float32)

