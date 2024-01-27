from random import randint
import numpy as np
from BrainBase import BrainBase
from SimpleNN import SimpleNN
from Color import COLOR_EMPTY, Color
from Enums.Direction import Direction
from Enums.MoveDirection import MoveDirection
from Enums.PointType import PointType
# from Field import Field
# from Food import Food
# from collections import deque


HEALTH_STEP = 1.0
HEALTH_TAIL = 20.0
TAIL_MIN_LENTH = 2
TAIL_MAX_LENTH = 16


class Snake:
    mapDirectionArrows = {Direction.UP: (0, -1),   Direction.DOWN: (0, 1),
                          Direction.LEFT: (-1, 0), Direction.RIGHT: (1, 0)}

    def __init__(self, body: list, brain: BrainBase, headViewDirection: Direction, color: Color = Color.randomColor(100, 200),  health: float = 100.0):
        self._body = body
        self._brain = brain
        self._headView = headViewDirection
        self._color = color
        self._health = health if (0.0 <= health <= 100.0) else 100.0

        self._alive = True
        self._age = 0

        self.mapDirectionArrows = {Direction.UP: (0, -1),   Direction.DOWN: (0, 1),
                                   Direction.LEFT: (1, 0), Direction.RIGHT: (1, 0)}

    def pointIsInSnake(self, point: tuple) -> bool:
        return len([1 for p in self._body if p == point]) > 0

    @property
    def viewRadius(self) -> Direction: return self._brain.viewRadius

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
    def head(self) -> tuple: return self._body[0]

    @property
    def tail(self) -> tuple: return self._body[-1]

    @property
    def len(self) -> int: return len(self._body)

    def die(self, setPoint):
        for p in self._body:
            setPoint(p, PointType.EMPTY, COLOR_EMPTY.toHTMLColor)
        self._body = list()
        self._alive = False

    def _removeTail(self, setPoint):
        if len(self._body) == 0:
            pass  # raise
        setPoint(self.tail, PointType.EMPTY, COLOR_EMPTY.toHTMLColor)
        self._body.pop()

    def getColorByBodyId(self, bodyId: int):
        if len(self._body) > 0 and 0 <= bodyId < len(self._body):
            if bodyId == 0:
                return self._color.darker().toHTMLColor
            else:
                return self._color.lighter(bodyId/len(self._body)).toHTMLColor
        else:
            pass  # raise

    def doOneStep(self, getPointType, setPoint, addSnakeToField):
        self._health -= HEALTH_STEP
        if self._health <= 0.0:
            if len(self._body) > TAIL_MIN_LENTH:
                self._removeTail(setPoint)
                self._health += HEALTH_TAIL
            else:
                return self.die(setPoint)
        action = self._brain.getDirection(self.getHeadView(getPointType))
        self._move(action, getPointType, setPoint)
        if len(self._body) > TAIL_MAX_LENTH:
            self._giveBirth()

    def _giveBirth(self, setPoint, addSnakeToField):
        pass  # TODO

    def _move(self, action: MoveDirection, getPointType, setPoint):
        if (not self._alive or self.len == 0 or action == MoveDirection.STAY):
            return True

        if (action == MoveDirection.LEFT):
            i = 1
        elif (action == MoveDirection.RIGHT):
            i = -1
        elif (action == MoveDirection.FORWARD):
            i = 0

        if i != 0:
            self._headView = Direction((int(self._headView)+i) % 4)

        h = self.head
        m = Snake.mapDirectionArrows[self._headView]
        new_head = (h[0]+m[0], h[1]+m[1])

        pt = getPointType(new_head)
        if (pt == PointType.WALL or pt == PointType.SNAKE):
            self.die(setPoint)
            return
        elif pt == PointType.FOOD:
            pass
        elif pt == PointType.EMPTY:
            self._removeTail(setPoint)

        self._body = [new_head] + self._body
        for i, p in enumerate(self._body):
            setPoint(p, PointType.SNAKE, self.getColorByBodyId(i))

    def getHeadView(self, getPointType, asPointType: bool = False) -> np.array:
        view = np.full((2*self._brain.viewRadius+1, 2 *
                       self._brain.viewRadius+1), PointType.EMPTY if asPointType else 0.0)
        head = self.head
        viewRadius = self._brain.viewRadius
        for x in range(view.shape[1]):
            for y in range(view.shape[0]):
                pt = getPointType((
                    head[0]-viewRadius+x, head[1]-viewRadius+y))
                view[x, y] = pt if asPointType else (
                    -1 if pt == PointType.SNAKE else int(pt))
        if self._headView != Direction.UP:
            view = np.rot90(view, int(self._headView))
        return view
