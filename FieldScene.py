from tkinter import NW, Tk, Canvas
from PIL import Image, ImageDraw, ImageTk
from Color import COLOR_FOOD, Color, COLOR_EMPTY

from Field import Field
# from Food import Food
from Snake import Snake


class FieldScene(object):
    def __init__(self, field: Field, canvasBlockSize: int, root: Tk, canvasField: Canvas):
        self._field = field
        self._canvasBlockSize = canvasBlockSize
        self._root = root
        self._canvasField = canvasField

        self._imgPILField = Image.new(mode="RGB", size=(
            self._field.width * self._canvasBlockSize, self._field.height * self._canvasBlockSize), color=COLOR_EMPTY.toTuple)
        self._drawPILField = ImageDraw.Draw(self._imgPILField)

        self._needRedraw = True
        self.setCaption()

    def drawAll(self):
        self._prepareSurf()
        if self._needRedraw:
            self._imgPILField.save("a1.png")
            self._canvasField.create_image(
                0, 0, anchor=NW, image=ImageTk.PhotoImage(self._imgPILField))
            # self._root.update_idletasks()            
            self._needRedraw = False
        self.setCaption()

    def setCaption(self):
        self._root.title(f"Field={self._field.width}x{self._field.height} Snakes={
            len(self._field.snakes)} Food={len(self._field.food)} Age={self._field.age}")

    def _pointToScreenRect(self, p) -> list:
        return (p[0]*self._canvasBlockSize, p[1]*self._canvasBlockSize,
                (p[0]+1)*self._canvasBlockSize, (p[1]+1)*self._canvasBlockSize)

    def _drawPoint(self, p: tuple, color: Color):
        ps=self._pointToScreenRect(p)
        self._drawPILField.rectangle(
            xy=ps, fill=color.toTuple, outline=COLOR_EMPTY.toTuple, width=1)
        # draw = ImageDraw.Draw(img)
        # draw.line((0, 0) + img.size, fill=220)
        # PIL.Image.putpixel(xy, value)

    def _prepareSurf(self):
        if self._field.needRedraw:
            self._imgPILField.paste(
               COLOR_EMPTY.toTuple, (0, 0, self._imgPILField.size[0], self._imgPILField.size[1]))

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
