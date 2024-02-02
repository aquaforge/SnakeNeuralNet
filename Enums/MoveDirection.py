from enum import Enum, unique


@unique
class MoveDirection(Enum):
    STAY = 0
    LEFT = 1
    FORWARD = 2
    RIGHT = 3

    def __int__(self):
        return self.value
