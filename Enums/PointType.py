from enum import Enum, unique


@unique
class PointType(Enum):
    WALL = -1
    EMPTY = 0
    FOOD = 1
    SNAKE = 2
