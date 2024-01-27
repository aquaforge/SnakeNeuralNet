import json
from json import JSONEncoder
import numpy as np


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyArrayEncoder, self).default(obj)


a = np.array([[11,  22, 33], [44,  55, 66], [77, 88,  99]])
b = json.dumps(a, cls=NumpyArrayEncoder).replace(" ","")
print(b)
c = np.array(json.loads(b))
print(c)
