# import json
# from json import JSONEncoder
# import numpy as np
# from NumpyArrayEncoder import NumpyArrayEncoder
# from db import DbOperations

# # a = np.array([[11,  22, 33], [44,  55, 66], [77, 88,  99]])
# # b = json.dumps(a, cls=NumpyArrayEncoder).replace(" ", "")
# # print(b)
# # c = np.array(json.loads(b))
# # print(c)

# if __name__ == '__main__':
#     pathData=[]
#     for i in range(50):
#         a = np.array([[i+1,  2, 3], [4,  5, 6], [7, 8,  9]])
#         b = json.dumps(a, cls=NumpyArrayEncoder).replace(" ", "")        
#         pathData.append ({"path": b,"result": i % 4, "viewSize":3})

#     dbo=DbOperations()
#     dbo.addBulk(pathData)
#     print (dbo.getCountRows())


import random

for i in range(5):
    print (random.randint(2, 7))
