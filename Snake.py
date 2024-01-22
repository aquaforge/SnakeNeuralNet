from random import randint
from SimpleNN import SimpleNN
import numpy as np
from Color import Color
from Enums.Direction import Direction
from Enums.MoveDirection import MoveDirection
from Enums.Point2D import Point2D
from collections import deque
from Enums.PointType import PointType


HEALTH_STEP = 1.0
HEALTH_TAIL = 20.0
TAIL_MIN_LENTH = 2
SNAKE_VIEW_RADIUS = 2


class Snake:
    def __init__(self, body: list, brain: SimpleNN, headViewDirection: Direction, color: Color,  health: float = 100.0):
        self._body = body
        self._headView = headViewDirection
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

        self.mapDirectionArrows = {Direction.UP: Point2D(-1, 0),   Direction.DOWN: Point2D(1, 0),
                                   Direction.LEFT: Point2D(0, -1), Direction.RIGHT: Point2D(0, 1)}

    @property
    def headViewDirection(self) -> Direction: return self._headView

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

    def die(self, matrixField: np.array) -> bool:
        self._alive = False
        for i in range(len(self._body)):
            self._removeTail(matrixField)
        return self._changed

    def _removeTail(self, matrixField: np.array):
        matrixField[self._body[-1].h, self._body[-1].w] = PointType.EMPTY
        self._body.pop()
        self._changed = True

    def doOneStep(self, matrixField: np.array, food: set) -> bool:
        self._changed = False
        self._health -= HEALTH_STEP
        if self._health <= 0.0:
            if len(self._body) > TAIL_MIN_LENTH:
                self._removeTail(matrixField)
                self._health += HEALTH_TAIL
            else:
                return self.die(matrixField)

        view = np.full((2*SNAKE_VIEW_RADIUS+1, 2*SNAKE_VIEW_RADIUS+1), 0.0)
        head_in_view = Point2D(SNAKE_VIEW_RADIUS, SNAKE_VIEW_RADIUS)
        head = self.head
        for i in range(view.shape[0]):
            for j in range(view.shape[1]):
                h = 0
                w = 0
                if self._headView == Direction.UP:
                    h = head.h-(i-head_in_view.h)
                    w = head.w-(j-head_in_view.w)
                elif self._headView == Direction.DOWN:
                    h = head.h+(i-head_in_view.h)
                    w = head.w+(j-head_in_view.w)
                elif self._headView == Direction.LEFT:
                    h = head.h-(j-head_in_view.w)
                    w = head.w-(i-head_in_view.h)
                elif self._headView == Direction.RIGHT:
                    h = head.h+(j-head_in_view.w)
                    w = head.w+(i-head_in_view.h)


                pointType = self._getMatrixPointType(
                    Point2D(h, w), matrixField)
                if pointType == PointType.SNAKE or pointType == PointType.WALL:
                    view[i, j] = -1.0
                elif pointType == PointType.FOOD:
                    view[i, j] = 1.0

        input_vector = np.hstack(
            (np.array([self._health/100, self.len/16]), view.flatten()))
        input_vector = input_vector.reshape(1, input_vector.size)

        output_vector = self._brain.predict(input_vector, verbose=0)
        action = MoveDirection(output_vector.argmax())

        self._move(action, matrixField, food)
        return self._changed

    def _getMatrixPointType(self, p: Point2D, matrixField: np.array) -> PointType:
        if p.h < 0 or p.w < 0 or p.h > matrixField.shape[0]-1 or p.w > matrixField.shape[1]-1:
            return PointType.WALL
        return matrixField[p.h, p.w]

    def _move(self, action: MoveDirection, matrixField: np.array,  food: set):
        if (not self._alive or self.len == 0 or action == MoveDirection.STAY):
            return True

        if (action == MoveDirection.LEFT):
            i = -1
        elif (action == MoveDirection.RIGHT):
            i = 1
        elif (action == MoveDirection.FORWARD):
            i = 0

        if i == 0:
            new_headView = self._headView
        else:
            # i = (int(self._headView)+i) % 4
            new_headView = Direction((int(self._headView)+i) % 4)

        head = self.head
        new_head = head + self.mapDirectionArrows[new_headView]

        headPointType = self._getMatrixPointType(new_head, matrixField)
        if (headPointType == PointType.WALL or headPointType == PointType.SNAKE):
            self.die(matrixField)
            return True
        elif headPointType == PointType.FOOD:
            food.remove(new_head)
        elif headPointType == PointType.EMPTY:
            self._removeTail(matrixField)

        self._body = [new_head] + self._body
        matrixField[new_head.h, new_head.w] = PointType.SNAKE

        self._headView = new_headView
        self._changed = True
