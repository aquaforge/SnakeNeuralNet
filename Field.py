from random import randint
from statistics import mean
from Color import COLOR_EMPTY, COLOR_FOOD, COLOR_WALL
from Enums.PointType import PointType
from Snake import Snake
from DbTrainData import DbTrainData


class Field:

    def __init__(self, width: int, height: int):
        self._width = width  # это слева направо
        self._height = height  # это сверху вниз

        self._maxFoodCount = int(0.01 * width * height)  # 0.01
        self._foodCount = 0

        self._snakes = set()
        self._age = 0
        self._needRedraw = True
        self.__selectedSnake = None

        self.__fieldData = [[(PointType.EMPTY, COLOR_EMPTY.toHTMLColor) for h in range(
            height)] for w in range(width)]

    def selectSnakeByPoint(self, p: tuple):
        for snake in self._snakes:
            if snake.pointIsInSnake(p):
                self.selectedSnake = snake
                return
        self.selectedSnake = None

    @property
    def selectedSnake(self):
        return self.__selectedSnake

    @selectedSnake.setter
    def selectedSnake(self, snake: Snake):
        self.__selectedSnake = snake
        self._needRedraw = True

    def pointInField(self, p: tuple) -> bool:
        return 0 <= p[0] < self._width and 0 <= p[1] < self._height

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
            ptOld, colorOld = self.__fieldData[p[0]][p[1]]
            if ptOld == pt and colorOld == colorHTML:
                return
            if ptOld == pt:
                self.__fieldData[p[0]][p[1]] = (pt, colorHTML)
                return

            if ptOld == PointType.FOOD and pt in (
            PointType.EMPTY, PointType.SNAKE, PointType.WALL, PointType.SNAKE_HEAD):
                self._foodCount -= 1
                self.__fieldData[p[0]][p[1]] = (pt, colorHTML)
                return

            if pt == PointType.FOOD and ptOld in (
            PointType.EMPTY, PointType.SNAKE, PointType.WALL, PointType.SNAKE_HEAD):
                self._foodCount += 1
                self.__fieldData[p[0]][p[1]] = (pt, colorHTML)
                return

            self.__fieldData[p[0]][p[1]] = (pt, colorHTML)

    @property
    def foodCount(self):
        return self._foodCount

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def age(self):
        return self._age

    @property
    def food(self):
        return self._food

    @property
    def snakes(self):
        return self._snakes

    @property
    def needRedraw(self):
        return self._needRedraw

    def setRedrawed(self):
        self._needRedraw = False

    def doOneStep(self):
        self._needRedraw = True
        self._age += 1

        for snake in self._snakes.copy():
            snake.doOneStep(self.getPointType, self.setPoint,
                            self.addSnakeToField)

        deletedSnakes = set(snake for snake in self._snakes if (
                not snake.alive or snake.len == 0))
        if len(deletedSnakes) > 0:
            self._snakes -= deletedSnakes

        self.addFood()

        if len(Snake.pathData) > 1000:
            self._saveToDB()

    def _saveToDB(self):
        if len(Snake.pathData) > 0:
            l = list(Snake.pathData.values()).copy()
            Snake.pathData = dict()
            dbo = DbTrainData()
            dbo.addBulkTrainData(l)

    def getAverageRank(self) -> list:
        r = dict()
        for i in range(1, 15):
            l = [sn.rankPersent for sn in self._snakes if sn.viewRadius == i]
            if len(l) > 0:
                r[i] = round(mean(l), 2)
        return sorted(r.items(), key=lambda item: item[0])

    def __del__(self):
        # self._saveToDB()
        pass

    def __setSelectedRandom(self):
        for sn in self._snakes:
            if sn.alive and sn.len > 0:
                self.selectedSnake = sn
                break

    def addFood(self):
        c = COLOR_FOOD.toHTMLColor
        wrongCount = 0
        while (self._foodCount < self._maxFoodCount and wrongCount < 100):
            x = randint(0, self._width)
            y = randint(0, self._height)
            if self.getPointType((x, y)) == PointType.EMPTY:
                self.setPoint((x, y), PointType.FOOD, c)
            else:
                wrongCount += 1

    def addSnakeToField(self, snake: Snake):
        if snake.alive and snake.len > 0:
            for p in snake.body:
                if self.getPointType(p) != PointType.EMPTY:
                    pass  # raise

            for i, p in enumerate(snake.body):
                self.setPoint(p, (PointType.SNAKE_HEAD if i ==
                                                          0 else PointType.SNAKE), snake.getColorByBodyId(i))

            self._snakes.add(snake)
            # self.selectedSnake = snake
