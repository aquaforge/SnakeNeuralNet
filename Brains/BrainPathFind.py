import numpy as np
from Brains.BrainBase import BrainBase
from Enums.MoveDirection import MoveDirection


class BrainPathFind (BrainBase):
    FOOD_REPLACE = -9  # less than -5

    def __init__(self, viewRadius: int):
        super().__init__(viewRadius)

    def _getSimpleDirection(self, view: np.array) -> MoveDirection:
        if view[self._viewRadius, self._viewRadius-1] >=0:
            return MoveDirection.FORWARD
        elif view[self._viewRadius-1, self._viewRadius] >=0:
            return MoveDirection.LEFT
        elif view[self._viewRadius+1, self._viewRadius] >=0:
            return MoveDirection.RIGHT
        else:
            return MoveDirection.STAY

    def getDirection(self, view: np.array) -> MoveDirection:
        '''view: np 2D matrix WALL:-1, FOOD:1, EMPTY:0, START:SENTER'''

        if 1 not in view:
            return self._getSimpleDirection(view)
        else:
            startPoint = (self._viewRadius, self._viewRadius)
            pf = np.copy(view).T
            pf[pf == 1] = BrainPathFind.FOOD_REPLACE

            #print(pf)
            endPoint = self._prepareWavePath(startPoint, pf)
            if endPoint == None:
                return self._getSimpleDirection(view)
            else:
                #print(pf)
                path = [endPoint[::-1]]
                p = endPoint
                stepCounter = 0
                while p != startPoint and stepCounter < 1000:
                    # print(path)
                    stepCounter += 1
                    for i, j in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                        n = (p[0]+i, p[1]+j)
                        if 0<=n[0]<pf.shape[0] and 0<=n[1]<pf.shape[1]:
                            if pf[n[0], n[1]]+1 == pf[p[0], p[1]]:
                                path = [n[::-1]]+path
                                p = n
                                break
                #print(path)
                if len(path) == 1:
                    path
                    # raise
                (i1,j1), (i2,j2) = path[0], path[1]
                if i1 < i2:
                    return MoveDirection.RIGHT
                elif i1 > i2:
                    return MoveDirection.LEFT
                elif j1 > j2:
                    return MoveDirection.FORWARD
                else:
                    return MoveDirection.STAY

    def _prepareWavePath(self, start: tuple, pf: np.array) -> tuple:
        level = 10
        pf[start[0], start[1]] = level
        wave = [start]
        stepCounter = 0
        while len(wave) > 0 and stepCounter < 1000:
            # print(pf)
            # print(wave)
            stepCounter += 1
            level += 1
            wave_new = []
            for w in wave:
                for i, j in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    p = (w[0]+i, w[1]+j)
                    if 0 <= p[0] < pf.shape[0] and 0 <= p[1] < pf.shape[1]:
                        if pf[p[0], p[1]] == BrainPathFind.FOOD_REPLACE:
                            pf[p[0], p[1]] = level
                            return (p[0], p[1])
                        elif pf[p[0], p[1]] == 0:
                            wave_new.append((p[0], p[1]))
                            pf[p[0], p[1]] = level
            wave = wave_new
        return None

