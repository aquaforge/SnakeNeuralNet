from random import randint
import numpy as np
from SimpleNN import SimpleNN
from Color import Color
from Enums.Direction import Direction
from Enums.MoveDirection import MoveDirection
from Enums.PointType import PointType
# from Field import Field
# from Food import Food
# from collections import deque


HEALTH_STEP = 1.0
HEALTH_TAIL = 20.0
TAIL_MIN_LENTH = 2


class Snake:
    def __init__(self, body: list, viewRadius: int, brain: SimpleNN, headViewDirection: Direction, color: Color = Color.randomColor(100, 200),  health: float = 100.0):
        self._body = body
        self._viewRadius = viewRadius
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
    def len(self) -> int: return len(self._body)

    def die(self, food, setPoint):
        for p in self._body:
            setPoint()
            food.add(p)
        self._body = list()
        self._alive = False

    def _removeTail(self):
        self._body.pop()

    def getColorByBodyId(self, bodyId: int):
        if len(self._body) > 0 and 0 <= bodyId < len(self._body):
            if bodyId == 0:
                return self._color.darker().toHTMLColor
            else:
                return self._color.lighter(bodyId/len(self._body)).toHTMLColor
        else:
            pass  # raise

    def doOneStep(self, food: set, getPointType, setPoint):
        self._health -= HEALTH_STEP
        if self._health <= 0.0:
            if len(self._body) > TAIL_MIN_LENTH:
                self._removeTail()
                self._health += HEALTH_TAIL
            else:
                return self.die(food, setPoint)

        view = np.full((2*self._viewRadius+1, 2*self._viewRadius+1), 0.0)
        # head_in_view = (SNAKE_VIEW_RADIUS, SNAKE_VIEW_RADIUS)

        head = self.head
        for x in range(view.shape[1]):
            for y in range(view.shape[0]):
                pt = getPointType((
                    head[0]-self._viewRadius+x, head[1]-self._viewRadius+y))
                view[y, x] = int(pt)

        if self._headView != Direction.UP:
            view = np.rot90(view, int(self._headView))

        input_vector = view.flatten()
        input_vector = input_vector.reshape(1, input_vector.size)

        output_vector = self._brain.predict(input_vector, verbose=0)
        action = MoveDirection(output_vector.argmax())
        self._move(action, food, getPointType)

    def _move(self, action: MoveDirection, food: set, getPointType):
        if (not self._alive or self.len == 0 or action == MoveDirection.STAY):
            return True

        if (action == MoveDirection.LEFT):
            i = -1
        elif (action == MoveDirection.RIGHT):
            i = 1
        elif (action == MoveDirection.FORWARD):
            i = 0

        if i != 0:
            self._headView = Direction((int(self._headView)+i) % 4)

        h = self.head
        m = self.mapDirectionArrows[self._headView]
        new_head = (h[0]+m[0], h[1]+m[1])

        pt = getPointType(new_head)
        if (pt == PointType.WALL or pt == PointType.SNAKE):
            self.die(food)
            return
        elif pt == PointType.FOOD:
            food.remove(new_head)
        elif pt == PointType.EMPTY:
            self._removeTail()

        self._body = [new_head] + self._body
