from enum import Enum, unique


@unique
class PointType(Enum):
    SNAKE_HEAD = -3
    SNAKE = -2
    WALL = -1
    EMPTY = 0
    FOOD = 1

    def __int__(self):
        return self.value
