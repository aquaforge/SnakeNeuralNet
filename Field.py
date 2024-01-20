import numpy as np
import datetime
from Color import Color, COLOR_EMPTY, COLOR_WALL, COLOR_FOOD
from Enums.Point2D import Point2D
from Enums.PointType import PointType
from Snake import Snake


class Field:
    def __init__(self, width: int, height: int, snakes: map, food: map, maxFood: int):
        self._width = width
        self._height = height

        self._age = 0
        self._need_redraw = True

        self._snakes = snakes
        self._food = food
        self._maxFood = maxFood
        self._prepareMatrixField()
        self.getMatrixColor()


    @property
    def age(self): return self._age

    @property
    def width(self): return self._width

    @property
    def height(self): return self._height

    @property
    def snakeCount(self) -> int: return len(self._snakes)

    @property
    def foodCount(self): return len(self._food)

    @property
    def maxFood(self) -> int: return self._maxFood

    @property
    def maxFood(self, val: int):
        self._maxFood = val

    @property
    def matrixField(self) -> np.array: return self._matrixField

    @property
    def matrixColor(self) -> np.array: return self._matrixColor

    @property
    def need_redraw(self):         return self._need_redraw

    def setRedrawed(self):
        self._need_redraw = False     

    def _prepareMatrixField(self):
        self._matrixField = np.full(
            (self._height, self._width), PointType.EMPTY)
        self._matrixField[0] = [PointType.WALL]*self._matrixField.shape[1]
        self._matrixField[-1] = self._matrixField[0]
        self._matrixField[:, 0] = [PointType.WALL]*self._matrixField.shape[0]
        self._matrixField[:, -1] = self._matrixField[:, 0]

        for food in self._food:
            self._matrixField[food.x, food.y] = PointType.FOOD

        for snake in self._snakes:
            if snake.alive:
                size = snake.len
                if size > 0:
                    for i in range(size):
                        self._matrixField[snake.body[i].x,
                                          snake.body[i].y] = PointType.SNAKE

    def getMatrixColor(self) -> np.array:
        if self._need_redraw:
            self._matrixColor = np.full(
                (self._height, self._width), COLOR_EMPTY)
            self._matrixColor[0] = [COLOR_WALL]*self._matrixColor.shape[1]
            self._matrixColor[-1] = self._matrixColor[0]
            self._matrixColor[:, 0] = [COLOR_WALL]*self._matrixColor.shape[0]
            self._matrixColor[:, -1] = self._matrixColor[:, 0]

            for food in self._food:
                self._matrixColor[food.x, food.y] = COLOR_FOOD

            for snake in self._snakes:
                if snake.alive and snake.len > 0:
                    for i in range(snake.len):
                        self._matrixColor[snake.body[i].x, snake.body[i].y] = snake.color.adjustColor(
                            i, snake.len)
            self._need_redraw = False
        print ('567')    
        return self._matrixColor

    def do_one_step(self):
        self._age += 1
        self._need_redraw = False
        for snake in self._snakes:
            if snake.doOneStep(self._matrixField):
                self._need_redraw = True

        deletedSnakes = set(snake for snake in self._snakes if not snake.alive)
        if len(deletedSnakes) > 0:
            self._snakes -= deletedSnakes
            self._need_redraw = True

        if self._need_redraw:
            self.getMatrixColor()
