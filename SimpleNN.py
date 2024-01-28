from dataclasses import dataclass
import json
import numpy as np
import jsonpickle
import jsonpickle.ext.numpy as jsonpickle_numpy
jsonpickle_numpy.register_handlers()


class ActivationBase():
    @staticmethod
    def activation(x):
        raise NotImplemented("class ActivationBase")

    @staticmethod
    def derivative(x):
        raise NotImplemented("class ActivationBase")


class ActivationSigmoid():
    @staticmethod
    def activation(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def derivative(x):
        return x * (1 - x)


class ActivationRelu():
    @staticmethod
    def activation(x):
        return np.where(x > 0, x, 0)

    @staticmethod
    def derivative(x):
        return np.greater(x, 0).astype(int)


class ActivationNone():
    @staticmethod
    def activation(x):
        return x

    @staticmethod
    def derivative(x):
        return 0


class ActivationSoftmax():  # https://eli.thegreenplace.net/2016/the-softmax-function-and-its-derivative/
    @staticmethod
    def activation(x):
        '''stable version'''
        exps = np.exp(x - np.max(x))
        return exps / np.sum(exps)


@dataclass
class Layer():
    nodesCount: int
    activationClass: ActivationBase = None
    useBias: bool = True


@dataclass
class LayerExtended(Layer):
    weights: np.array = None
    val: np.array = None
    valActivated: np.array = None


class SimpleNN:
    def __init__(self, layers: list, learningRate: float = 0.01):
        self._learningRate = learningRate
        self._layers = list()

        for i, layer in enumerate(layers):
            if i == 0:
                layer.useBias = False
                layer.weights = None
                layer.activation = None
                w = None
            else:
                if layer.activationClass == None:
                    layer.activationClass = ActivationNone
                else:
                    if i != len(layers)-1:
                        if isinstance(layer.activationClass, ActivationSoftmax):
                            raise NotImplemented("Softmax for hidden layer")
                w = np.random.random(
                    size=(layer.nodesCount, layers[i-1].nodesCount + (1 if layer.useBias else 0)))
            self._layers.append(LayerExtended(nodesCount=layer.nodesCount,
                                              activationClass=layer.activationClass, useBias=layer.useBias, weights=w))

    def predict(self, inputVector: np.array):
        # val = np.array(inputVector, ndmin=2).T
        self._layers[0].val = inputVector
        self._layers[0].valActivated = inputVector
        for i in range(1, len(self._layers)):
            # print(self._layers[i-1].valActivated)
            if self._layers[i].useBias:
                val = np.append(self._layers[i-1].valActivated, [[0.99999]], 0)
                # print(val)
            else:
                val = self._layers[i-1].valActivated
            self._layers[i].val = np.dot(self._layers[i].weights, val)
            self._layers[i].valActivated = self._layers[i].activationClass.activation(
                self._layers[i].val)
        return self._layers[-1].valActivated

    def clearTemp(self):
        for i in range(1, len(self._layers)):
            self._layers[i].val = None
            self._layers[i].valActivated = None
        return {"learningRate": self._learningRate, "layers": self._layers}

    @staticmethod
    def mse_loss(y_true, y_pred):
        return ((y_true - y_pred) ** 2).mean()

    def trainEpoch(self, inputData: np.array, targetData: np.array, epochs: int = 1):
        '''inputData shape (60000,786)  targetData shape (60000,10)'''
        for e in range(epochs):
            pass

    def train(self, inputVector: np.array, targetVector: np.array):
        # inputs = np.array(inputs_list, ndmin=2).T
        # targets = np.array(targets_list, ndmin=2).T
        outputErrors = targetVector - self.predict(inputVector)

        # hidden_errors = numpy.dot(self.who.T, output_errors)
        # # update the weights for the links between the hidden and output layers
        # self.who += self.lr * numpy.dot((output_errors * final_outputs * (1.0 - final_outputs)), numpy.transpose(hidden_outputs))
        # # update the weights for the links between the input and hidden layers
        # self.wih += self.lr * numpy.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)), numpy.transpose(inputs))

    def encode(self) -> dict:
        self.clearTemp()
        return jsonpickle.encode(self)

    def info(self) -> dict:
        l = list()
        for layer in self._layers:
            d = dict()
            d["nodesCount"] = layer.nodesCount
            if layer.activationClass is None:
                d["activationClass"] = None
            else:
                d["activationClass"] = layer.activationClass.__name__
            d["useBias"] = layer.useBias
            l.append(d)

        w=dict()
        w["weigthAvg"] = json.dumps([round(l.weights.mean(), 6)
                    for l in self._layers if l.weights is not None])
        w["weigthMin"] = json.dumps([round(l.weights.min(), 6)
                    for l in self._layers if l.weights is not None])
        w["weigthMax"] = json.dumps([round(l.weights.max(), 6)
                    for l in self._layers if l.weights is not None])


        d = dict()
        d["config"] = json.dumps(l).replace(" ","")
        d["weigth"] = json.dumps(w).replace(" ","")
        d["data"] = self.encode()
        return d

    @staticmethod
    def decode(data: str):
        return jsonpickle.decode(data)
