from enum import Enum, unique

@unique
class MoveDirection(Enum):
    NONE = 0
    FORWARD = 1
    RIGHT = 2
    LEFT = 3

