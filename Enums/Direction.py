from enum import Enum, unique


@unique
class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __int__(self):
        return self.value



