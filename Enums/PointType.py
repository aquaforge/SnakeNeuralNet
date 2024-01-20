from enum import Enum, unique


@unique
class PointType(Enum):
    EMPTY = 0
    WALL = 1
    FOOD = 2
    SNAKE = 3
