import pygame as pg
from Color import COLOR_EMPTY
from Field import Field


class DrawScene():
    def __init__(self, sc: pg.Surface, field: Field, blockSize: int, marginInner: int,
                 marginOuter: int):
        self._sc = sc
        self._left = 0
        self._top = 0
        self._need_redraw = True

        self._surf = None
        self._field = field

        self._blockSize = blockSize
        self._marginInner = marginInner
        self._marginOuter = marginOuter
        self._get_surf_size()

    def _get_surf_size(self):
        self._draw_size = (
            2 * self._marginOuter - self._marginInner + self._field.width * (
                self._blockSize + self._marginInner),
            2 * self._marginOuter - self._marginInner + self._field.height * (
                self._blockSize + self._marginInner)
        )

    def draw(self):
        self._prepare_surf()
        if self._need_redraw:
            self._sc.fill(COLOR_EMPTY.toTuple)
            if self._surf is not None:
                self._sc.blit(self._surf, (self._left, self._top))
            pg.display.update()
            self._need_redraw = False
            #print("sc_redraw")

        pg.display.set_caption(f"Field={self._field.width}x{self._field.height} Snakes={
                               self._field.snakeCount} Food={self._field.foodCount} Age={self._field.age}")

    @property
    def left(self):
        return self._left

    @property
    def top(self):
        return self._top

    @left.setter
    def left(self, left: int):
        if self._left != left:
            self._need_redraw = True
            self._left = left

    @top.setter
    def top(self, top: int):
        if self._top != top:
            self._need_redraw = True
            self._top = top

    def _prepare_surf(self):
        changed = False
        if self._surf is None:
            self._surf = pg.Surface(self._draw_size)
            changed = True
        elif (self._surf.get_width(), self._surf.get_height()) != self._draw_size:
            self._surf = pg.Surface(self._draw_size)
            changed = True

        if changed or self._field.need_redraw:
            self._surf.fill((125, 125, 125))
            matrix = self._field.getMatrixColor(False)

            for h in range(self._field.height):
                for w in range(self._field.width):
                    pg.draw.rect(self._surf, matrix[h, w].toTuple, (
                        self._marginOuter + w *
                        (self._blockSize + self._marginInner),
                        self._marginOuter + h *
                        (self._blockSize + self._marginInner),
                        self._blockSize,
                        self._blockSize))

            self._field.setRedrawed()
            self._need_redraw = True
            #print('fff')