from abc import ABC, abstractmethod

import numpy as np
from Enums.MoveDirection import MoveDirection


class BrainBase (ABC):

    def __init__(self, viewRadius: int):
        self._viewRadius = viewRadius

    @property
    def viewRadius(self): return self._viewRadius

    @abstractmethod
    def getDirection(self, view: np.array) -> MoveDirection:
        pass

    @abstractmethod
    def toJsonStr(self) -> str:
        pass
