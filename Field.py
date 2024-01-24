from random import randint
from Enums.PointType import PointType
# from Food import Food
from Snake import Snake


class Field:
    def __init__(self, width: int, height: int):
        self._width = width  # это слева направо
        self._height = height  # это сверху вниз
        self._maxFoodCount = 0.05 * width * height

        self._food = set()
        self._snakes = set()
        self._age = 0
        self._needRedraw = True

    def pointIsInFood(self, point: tuple) -> bool:
        return len([1 for f in self._food if f == point]) > 0

    def pointIsInSnakes(self, point: tuple) -> bool:
        return len([1 for snake in self._snakes if snake.pointIsInSnake(point)]) > 0

    def getPointType(self, p: tuple):
        if 0 < p[0] < self._width and 0 < p[1] < self._height:
            if self.pointIsInFood(p):
                return PointType.FOOD
            elif self.pointIsInSnakes(p):
                return PointType.SNAKE
            else:
                return PointType.EMPTY
        else:
            return PointType.WALL

    @property
    def width(self): return self._width

    @property
    def height(self): return self._height

    @property
    def age(self): return self._age

    @property
    def food(self): return self._food

    @property
    def snakes(self): return self._snakes

    @property
    def needRedraw(self): return self._needRedraw

    def setRedrawed(self):
        self._needRedraw = False

    def doOneStep(self):
        self._needRedraw = True
        self._age += 1

        for snake in self._snakes:
            snake.doOneStep(self._food, self.getPointType)

        deletedSnakes = set(snake for snake in self._snakes if not snake.alive)
        if len(deletedSnakes) > 0:
            self._snakes -= deletedSnakes

        self.addFood()

    def addFood(self):
        wrongCount = 0
        while (len(self._food) < self._maxFoodCount and wrongCount < 100):
            x = randint(0, self._width)
            y = randint(0, self._height)
            if self.getPointType((x, y)) == PointType.EMPTY:
                self._food.add((x, y))
            else:
                wrongCount += 1
