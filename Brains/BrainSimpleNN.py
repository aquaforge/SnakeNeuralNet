import numpy as np
from Brains.BrainBase import BrainBase
from Enums.MoveDirection import MoveDirection
from SimpleNN import SimpleNN


class BrainSimpleNN (BrainBase):
    def __init__(self, viewRadius: int, model: SimpleNN):
        super().__init__(viewRadius)
        self._model = model

    def getDirection(self, input_vector: np.array) -> MoveDirection:
        output_vector = self._model.predict(input_vector, verbose=0)
        return MoveDirection(output_vector.argmax())

