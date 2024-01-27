from dataclasses import dataclass
from random import randint


@dataclass
class Color:
    r: int
    g: int
    b: int

    @property
    # convert to tuple(r,g,b)
    def toTuple(self) -> tuple: return (self.r, self.g, self.b)

    @property
    # convert to "#RRGGBB"
    def toHTMLColor(self) -> str: return "#%02x%02x%02x" % self.toTuple

    @staticmethod
    def randomColor(lFrom: int, lTo: int):
        c = [randint(lFrom, lTo) for i in range(3)]
        return Color(c[0], c[1], c[2])

    def lighter(self, val: float):
        c = [int(i+(230-i)*val/2) for i in self.toTuple]
        return Color(c[0], c[1], c[2])

    def darker(self, val: float = 0.7):
        return Color(int(self.r*val), int(self.g*val), int(self.b*val))


COLOR_FOOD = Color(255, 0, 0)
COLOR_SNAKE=Color(100,200,100)
COLOR_EMPTY = Color(210, 210, 210)
COLOR_WALL = Color(0, 0, 0)
COLOR_OUTLINE = Color(70, 70, 70)
COLOR_SELECTED = Color(50, 230, 50)


COLOR_SNAKE_RANGE = (100, 200)
