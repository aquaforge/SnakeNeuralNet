import numpy as np
from SimpleNN import ActivationNone, ActivationRelu, ActivationSigmoid, Layer, SimpleNN
import json
import pprint


l = list()
l.append(Layer(nodesCount=1))
l.append(Layer(nodesCount=3, activationClass=ActivationRelu, useBias=True))
l.append(Layer(nodesCount=1, activationClass=ActivationNone, useBias=False))
nn = SimpleNN(layers=l, learningRate=0.01)

y=np.random.random(size=(1,1))
o = nn.predict(y)
print(y, o)

for i in range(10000):
    inp=2*np.random.random(size=(1,1))
    nn.train(inp, -inp)

o = nn.predict(y)
print(y, o)

# s = nn.encode()
# newNN =  SimpleNN.decode(s)
# o2 = newNN.predict(inp)
# i2=newNN.info()
# print(o2)


# print(isinstance(ActivationRelu(), ActivationRelu))


# s = jsonpickle.encode(nn)
# newNN = jsonpickle.decode(s)
# print(s)
# pip install -U jsonpickle
