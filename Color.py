from dataclasses import dataclass


@dataclass
class Color:
    r: int
    g: int
    b: int

    @property
    def toTuple(self): return (self.r, self.g, self.b)

    def adjustColor(self, pos: int, size: int, isEndWhite: bool = True):
        end = 255 if isEndWhite else 0
        r = self.r+(end-self.r)*pos/size/2
        g = self.g+(end-self.g)*pos/size/2
        b = self.b+(end-self.b)*pos/size/2
        return Color(r, g, b)


COLOR_EMPTY = Color(210, 210, 210)
COLOR_WALL = Color(0, 0, 0)
COLOR_FOOD = Color(255, 0, 0)
COLOR_SNAKE_RANGE = (70, 200)
