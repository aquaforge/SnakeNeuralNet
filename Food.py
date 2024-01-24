'''
from random import randint
from Enums.PointType import PointType
from Field import Field


class Food:
    def __init__(self, width:int, height:int):
        self._width = width
        self._height = height
        self._maxFoodCount = 0.05 * width * height
        self._food = set()

    def pointIsInFood(self, p: tuple) -> bool:
        return len([f for f in self._food if f == p]) > 0

    def addFood(self, field: Field):
        wrongCount = 0
        while (len(self._food) < self._maxFoodCount and wrongCount < 50):
            x = randint(0, self._height)
            y = randint(0, self._width)
            if field.getPointType((x, y)) == PointType.EMPTY:
                self._food.add((x, y))
            else:
                wrongCount += 1
'''