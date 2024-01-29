import numpy as np
from SimpleNN import ActivationRelu, ActivationSigmoid, Layer, SimpleNN, ActivationSoftmax
from NumpyArrayEncoder import NumpyArrayEncoder
import json
import pprint


l = list()
l.append(Layer(nodesCount=5))
l.append(Layer(nodesCount=3, activationClass=ActivationRelu, useBias=True))
l.append(Layer(nodesCount=4, activationClass=ActivationRelu, useBias=False))
nn = SimpleNN(layers=l, learningRate=0.01)

inp=np.random.random(size=(5,1))
o1 = nn.predict(inp)
i1=nn.info()
print(o1)

s = nn.encode()
newNN =  SimpleNN.decode(s)
o2 = newNN.predict(inp)
i2=newNN.info()
print(o2)


# print(isinstance(ActivationRelu(), ActivationRelu))


# s = jsonpickle.encode(nn)
# newNN = jsonpickle.decode(s)
# print(s)
# pip install -U jsonpickle
