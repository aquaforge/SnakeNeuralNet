import pygame as pg
from Color import COLOR_FOOD, Color, COLOR_EMPTY

from Field import Field
#from Food import Food
from Snake import Snake


class FieldScene(object):
    CanvasBlockSize = 30
    CanvasMargin = 1

    '''
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FieldScene, cls).__new__(cls)
        return cls.instance
    '''

    def __init__(self, disp: pg.display, field: Field):
        self._disp = disp
        self._field = field

        self._left = 5
        self._top = 5
        self._surf = None
        self._needRedraw = True

        self._draw_size = (
            2 * FieldScene.CanvasMargin - FieldScene.CanvasMargin + field.width * (
                FieldScene.CanvasBlockSize + FieldScene.CanvasMargin),
            2 * FieldScene.CanvasMargin - FieldScene.CanvasMargin + field.height * (
                FieldScene.CanvasBlockSize + FieldScene.CanvasMargin)
        )
        self.setCaption()

    @property
    def left(self):
        return self._left

    @property
    def top(self):
        return self._top

    @left.setter
    def left(self, left: int):
        if self._left != left:
            self._needRedraw = True
            self._left = left

    @top.setter
    def top(self, top: int):
        if self._top != top:
            self._needRedraw = True
            self._top = top

    def _pointToScreenCoord(self, p) -> list:
        return [p[0]*FieldScene.CanvasBlockSize, p[1]*FieldScene.CanvasBlockSize, (p[0]+1)*FieldScene.CanvasBlockSize, (p[1]+1)*FieldScene.CanvasBlockSize]

    def drawAll(self):
        self._prepareSurf()
        if self._needRedraw:
            self._disp.fill(COLOR_EMPTY.darker().toTuple)
            self._disp.blit(self._surf, (self._left, self._top))
            pg.display.update()
            self._needRedraw = False
        self.setCaption()

    def setCaption(self):
        pg.display.set_caption(f"Field={self._field.width}x{self._field.height} Snakes={
            len(self._field.snakes)} Food={len(self._field.food)} Age={self._field.age}")

    def _drawPoint(self, p: tuple, c: Color):
        pg.draw.rect(self._surf, c.toTuple, (
            FieldScene.CanvasMargin + p[0] *
            (FieldScene.CanvasBlockSize + FieldScene.CanvasMargin),
            FieldScene.CanvasMargin + p[1] *
            (FieldScene.CanvasBlockSize + FieldScene.CanvasMargin),
            FieldScene.CanvasBlockSize,
            FieldScene.CanvasBlockSize))

    def _prepareSurf(self):
        changed = False
        if self._surf is None:
            self._surf = pg.Surface(self._draw_size)
            changed = True

        if changed or self._field.needRedraw:
            self._surf.fill(COLOR_EMPTY.toTuple)

            for p in self._field.food:
                self._drawPoint(p, COLOR_FOOD)

            for snake in self._field.snakes:
                if snake.alive and snake.len > 0:
                    for i, p in enumerate(snake.body):
                        if i == 0:
                            self._drawPoint(p, snake.color.darker())
                        else:
                            self._drawPoint(
                                p, snake.color.lighter(i/snake.len))

            self._field.setRedrawed()
            self._needRedraw = True
            # print('fff')
