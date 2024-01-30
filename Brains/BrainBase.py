import json
import numpy as np
from Enums.MoveDirection import MoveDirection


class BrainBase():
    def __init__(self, viewRadius: int):
        self._viewRadius = viewRadius

    @property
    def viewRadius(self): return self._viewRadius

    def getDirection(self, view: np.array) -> MoveDirection:
        '''view: np 2D matrix'''
        if view[self._viewRadius, self._viewRadius-1] != -1:
            return MoveDirection.FORWARD
        elif view[self._viewRadius-1, self._viewRadius] != -1:
            return MoveDirection.LEFT
        elif view[self._viewRadius+1, self._viewRadius] != -1:
            return MoveDirection.RIGHT
        else:
            return MoveDirection.STAY

    @property
    def getInfoDict(self):
        return {"brainType": type(self).__name__,
                "viewRadius": self._viewRadius}

    @property
    def toJsonStr(self) -> str:
        return json.dumps(self.getInfoDict)
