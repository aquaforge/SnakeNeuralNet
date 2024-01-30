from math import cos, sin
from random import random
import numpy as np
from SimpleNN import ActivationNone, ActivationRelu, ActivationSigmoid, Layer, SimpleNN
import json
import pprint
import matplotlib.pyplot as plt
import matplotlib as mpl


# y=sin(x * pi * 3.5) + 1pip
def fun(x):
    # return sin(x*3.1415926*3.5) #+1.0
    return cos(x*3.1415926*3.5) #+1.0


l = list()
l.append(Layer(nodesCount=1))
l.append(Layer(nodesCount=15, activationClass=ActivationRelu, useBias=True))
l.append(Layer(nodesCount=5, activationClass=ActivationRelu, useBias=True))
l.append(Layer(nodesCount=1, activationClass=ActivationNone, useBias=False))
nn = SimpleNN(layers=l, learningRate=0.01)

# y=2*np.random.random(size=(2,1))-1
# o = nn.predict(y)
# print(np.sum(y), np.sum(o))

# for i in range(10000):
#     inp=2*np.random.random(size=(2,1))-1
#     nn.train(inp, np.array([np.sum(inp)]))

# o = nn.predict(y)
# print(np.sum(y), np.sum(o))


y=random()
o = nn.predict( np.array([y]))
# print(fun(y), np.sum(o))

for i in range(90000):
    v=random()
    nn.train(np.array([v]), np.array([fun(v)]))

o = nn.predict( np.array([y]))
# print(fun(y), np.sum(o))

# https://skillbox.ru/media/code/biblioteka-matplotlib-dlya-postroeniya-grafikov/?ysclid=lrz9bhflcp714131757
t=[i/100 for i in range(100)]
f=[fun(x) for x in t]
n=[np.sum(nn.predict(np.array([x]))) for x in t]

print(SimpleNN.mseLoss(f,n))

plt.plot(t, f, 'r') # plotting t, a separately 
plt.plot(t, n, 'b') # plotting t, b separately 
plt.show()



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
