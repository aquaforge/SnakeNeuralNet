from random import randint
from Color import COLOR_EMPTY, COLOR_FOOD, COLOR_WALL
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
        self._selectedSnake=None

        self.__fieldData = [[(PointType.EMPTY, COLOR_EMPTY.toHTMLColor) for h in range(
            height)] for w in range(width)]

    def pointInField(self, p: tuple) -> bool:
        return 0 < p[0] < self._width and 0 < p[1] < self._height

    def getPointType(self, p: tuple) -> PointType:
        if not self.pointInField(p):
            return PointType.WALL
        else:
            pt, _ = self.__fieldData[p[0]][p[1]]
            return pt

    def getPointColorHTML(self, p: tuple) -> str:
        if not self.pointInField(p):
            return COLOR_WALL.toHTMLColor
        else:
            _, c = self.__fieldData[p[0]][p[1]]
            return c

    def setPoint(self, p: tuple, pt: PointType, colorHTML: str):
        if not self.pointInField(p):
            return  # RAISE
        else:
            if (pt, colorHTML) != oldPT:
                self.__fieldData[p[0]][p[1]] = (pt, colorHTML)
                self._needRedraw

    @property
    def selectedSnake(self):return self._selectedSnake

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
            snake.doOneStep(self._food, self.getPointType, self.setPoint)

        deletedSnakes = set(snake for snake in self._snakes if (
            not snake.alive or snake.len == 0))
        if len(deletedSnakes) > 0:
            self._snakes -= deletedSnakes

        self.addFood()

    def addFood(self):
        c = COLOR_FOOD.toHTMLColor
        wrongCount = 0
        while (len(self._food) < self._maxFoodCount and wrongCount < 100):
            x = randint(0, self._width)
            y = randint(0, self._height)
            if self.getPointType((x, y)) == PointType.EMPTY:
                self._food.add((x, y))
                self.__fieldData[x][y] = (PointType.FOOD, c)
            else:
                wrongCount += 1

    def addSnakeToField(self, snake: Snake):
        if snake.alive and snake.len > 0:
            for p in snake.body:
                if self.getPointType(p) !=PointType.EMPTY:
                    pass # raise

            for i, p in enumerate(snake.body):
                self.setPoint(p, snake.getColorByBodyId(i))

            self._snakes.add(snake)
            self._selectedSnake = snake


