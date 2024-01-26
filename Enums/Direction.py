from enum import Enum, unique


@unique
class Direction(Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3

    def __int__(self):
        return self.value
    





