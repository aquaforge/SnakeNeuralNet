import numpy as np
from Brains.BrainBase import BrainBase
from Enums.MoveDirection import MoveDirection
from SimpleNN import SimpleNN


class BrainSimpleNN (BrainBase):
    def __init__(self, viewRadius: int, model: SimpleNN):
        super().__init__(viewRadius)
        self._model = model

    def getDirection(self, view: np.array) -> MoveDirection:
        '''view: np 2D matrix'''
        input_vector = view.flatten()
        input_vector = input_vector.reshape(1, input_vector.size)
        output_vector = self._model.predict(input_vector, verbose=0)
        return MoveDirection(output_vector.argmax())

    @property
    def toJsonStr(self) -> str: return "TBD"
