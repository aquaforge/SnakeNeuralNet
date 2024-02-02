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
        return np.greater(x, 0).astype(int).astype(float)


class ActivationNone():
    @staticmethod
    def activation(x):
        return x

    @staticmethod
    def derivative(x):
        return 1.0


'''
class ActivationSoftmax():  # https://eli.thegreenplace.net/2016/the-softmax-function-and-its-derivative/
    @staticmethod
    def activation(x):
        exps = np.exp(x - np.max(x))
        return exps / np.sum(exps)
'''


@dataclass
class Layer():
    nodesCount: int
    activationClass: ActivationBase = None
    useBias: bool = True


@dataclass
class LayerExtended(Layer):
    bias: np.array = None
    weights: np.array = None
    val: np.array = None
    valActivated: np.array = None
    gradients: np.array = None


class SimpleNN:
    def __init__(self, layers: list, id: int = None, learningRate: float = 0.01):
        self._id = id
        self._learningRate = learningRate
        self._layers = list()

        for i, layer in enumerate(layers):
            if i == 0:
                layer.useBias = False
                layer.weights = None
                layer.activation = None
                w = None
                b = None
            else:
                if layer.activationClass == None:
                    layer.activationClass = ActivationNone
                w = np.random.random(
                    size=(layer.nodesCount, layers[i - 1].nodesCount))
                b = np.random.random(size=(layer.nodesCount, 1))
            self._layers.append(LayerExtended(nodesCount=layer.nodesCount,
                                              activationClass=layer.activationClass, useBias=layer.useBias, bias=b,
                                              weights=w))

    def predict(self, inputVector):
        inputVector = np.array(inputVector).reshape(
            self._layers[0].nodesCount, 1)
        self._layers[0].val = inputVector
        self._layers[0].valActivated = inputVector
        for i in range(1, len(self._layers)):
            val = self._layers[i - 1].valActivated
            val = np.dot(self._layers[i].weights, val)
            if self._layers[i].useBias:
                val += self._layers[i].bias
            self._layers[i].val = val
            self._layers[i].valActivated = self._layers[i].activationClass.activation(
                val)
        return self._layers[-1].valActivated

    def clearTemp(self):
        for i in range(1, len(self._layers)):
            self._layers[i].val = None
            self._layers[i].valActivated = None
            self._layers[i].gradients = None
        return {"learningRate": self._learningRate, "layers": self._layers}

    @staticmethod
    def mseLoss(y_true, y_pred):
        return ((np.array(y_true) - np.array(y_pred)) ** 2).mean()

    def train(self, inputVector, targetVector):
        self._id = None
        inputVector = np.array(inputVector).reshape(
            self._layers[0].nodesCount, 1)
        targetVector = np.array(targetVector).reshape(
            self._layers[-1].nodesCount, 1)

        for i in range(len(self._layers) - 1, 0, -1):
            if i == len(self._layers) - 1:
                errors = targetVector - self.predict(inputVector)
            else:
                errors = np.dot(self._layers[i + 1].weights.T, errors)
            gradients = self._layers[i].activationClass.derivative(
                self._layers[i].valActivated)
            gradients *= errors
            gradients *= self._learningRate
            self._layers[i].gradients = gradients

        for i in range(1, len(self._layers)):
            if self._layers[i].useBias:
                self._layers[i].bias += self._layers[i].gradients
            a = self._layers[i].gradients
            b = self._layers[i - 1].valActivated.T
            self._layers[i].weights += np.dot(a, b)

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

        d = dict()
        d["config"] = json.dumps(l).replace(" ", "")
        d["data"] = self.encode()
        d["id"] = self._id
        return d

    @staticmethod
    def decode(data: str):
        return jsonpickle.decode(data)


'''
    def train(self, input_array, target_array):
        inputs = np.array(input_array).reshape(self.input_nodes, 1)
        targets = np.array(target_array).reshape(self.output_nodes, 1)

        hidden = np.dot(self.weights_ih, inputs) + self.bias_h
        hidden = self.sigmoid(hidden)

        outputs = np.dot(self.weights_ho, hidden) + self.bias_o
        outputs = self.sigmoid(outputs)

        output_errors = targets - outputs
        output_gradients = self.sigmoid_derivative(outputs)
        output_gradients *= output_errors
        output_gradients *= self.learning_rate

        hidden_errors = np.dot(self.weights_ho.T, output_errors)
        hidden_gradients = self.sigmoid_derivative(hidden)
        hidden_gradients *= hidden_errors
        hidden_gradients *= self.learning_rate

        self.weights_ih += np.dot(hidden_gradients, inputs.T)
        self.bias_h += hidden_gradients
        self.weights_ho += np.dot(output_gradients, hidden.T)
        self.bias_o += output_gradients

    def predict(self, input_array):
        inputs = np.array(input_array).reshape(self.input_nodes, 1)

        hidden = np.dot(self.weights_ih, inputs) + self.bias_h
        hidden = self.sigmoid(hidden)

        outputs = np.dot(self.weights_ho, hidden) + self.bias_o
        outputs = self.sigmoid(outputs)

        return outputs

'''
