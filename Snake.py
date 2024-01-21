from random import randint
from SimpleNN import SimpleNN
import numpy as np
from Color import Color
from Enums.Direction import Direction
from Enums.MoveDirection import MoveDirection
import Enums.Point2D as Point2D
from collections import deque
from Enums.PointType import PointType


HEALTH_STEP = 0.5
HEALTH_TAIL = 20.0
TAIL_MIN_LENTH = 2


class Snake:
    def __init__(self, body: list, brain: SimpleNN, headViewDirection: Direction, color: Color,  health: float = 100.0):
        self._body = body
        self._headViewDirection = headViewDirection
        self._color = color
        self._brain = brain

        if health > 100.0:
            self._health = 100.0
        elif health < 0.0:
            self._health = 100.0
        else:
            self._health = health

        self._alive = True
        self._age = 0
        self._changed = 0

    @property
    def headViewDirection(self) -> Direction: return self._headViewDirection

    @property
    def health(self) -> float: return self._health

    @property
    def color(self) -> Color: return self._color

    @property
    def age(self) -> int: return self._age

    @property
    def alive(self) -> bool: return self._alive

    @property
    def body(self) -> list: return self._body

    @property
    def head(self) -> Point2D: return self._body[0]

    @property
    def tail(self) -> Point2D: return self._body[-1]

    @property
    def len(self) -> int: return len(self._body)

    def die(self, val):
        self._alive = False

    def _removeTail(self, matrixField: np.array):
        matrixField[self._body[-1].x, self._body[-1].y] = PointType.EMPTY
        self._body.pop()
        self._changed = True

    def doOneStep(self, matrixField: np.array) -> bool:
        self._changed = False
        self._health -= HEALTH_STEP
        if self._health <= 0.0:
            if len(self._body) > TAIL_MIN_LENTH:
                self._removeTail(matrixField)
                self._health += HEALTH_TAIL
            else:
                for i in range(len(self._body)):
                    self._removeTail(matrixField)
                self._health = 0
                self._alive = False
                return self._changed

        # TODO np.rot90(a, k=2)
            
            
        return self._changed


'''
    def move(self, direction: MoveDirection):
        if (not self._alive or direction == MoveDirection.NONE):
            return

        old_head_type, new_head_type = self._new_types()
        self._map.point(self.head()).type = old_head_type
        new_head = self.head().adj(self._direc_next)
        self._body.appendleft(new_head)

        if not self._map.is_safe(new_head):
            self._dead = True
        if self._map.point(new_head).type == PointType.FOOD:
            self._map.rm_food()
        else:
            self._rm_tail()

        self._map.point(new_head).type = new_head_type
        self._direc = self._direc_next
        self._steps += 1
'''
