import numpy as np
from BrainBase import BrainBase
from Enums.MoveDirection import MoveDirection


class BrainPathFind (BrainBase):
    def __init__(self, viewRadius: int):
        super().__init__(viewRadius)

    def _getSimpleDirection(self, view: np.array) -> MoveDirection:
        if view[self._viewRadius, self._viewRadius-1] != -1:
            return MoveDirection.FORWARD
        elif view[self._viewRadius-1, self._viewRadius] != -1:
            return MoveDirection.LEFT
        elif view[self._viewRadius+1, self._viewRadius] != -1:
            return MoveDirection.RIGHT
        else:
            return MoveDirection.STAY

    def getDirection(self, view: np.array) -> MoveDirection:
        '''view: np 2D matrix'''
        if 1 not in view:
            return self._getSimpleDirection(view)
        else:
            pf = np.copy(view)
            pf[view == 1] = -100
            xy = self._prepareWavePath(self, pf)
            if xy == None:
                return self._getSimpleDirection(view)
            else:
                pass  # TODO

    def _prepareWavePath(self, start: tuple, pf: np.array) -> tuple:
        level = 100
        pf[start[0], start[1]] = level
        wave = [start]
        while len(wave) > 0:
            level += 1
            wave_new = []
            for x, y in wave:
                for i, j in [(0, -1), (0, 1), (1, 0), (1, 0)]:
                    x += i
                    y += j
                    if 0 <= x < pf.size[0] and 0 <= y < pf.size[0]:
                        if pf[x, y] == -100:
                            self.grid[x][y] = level
                            return (x, y)
                        elif pf[x, y] == 0:
                            wave_new.append((x, y))
            wave = wave_new
        return None

    @property
    def toJsonStr(self) -> str: return "TBD"
