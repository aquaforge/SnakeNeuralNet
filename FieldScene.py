from tkinter import Tk, Canvas
from PIL import Image
from Color import COLOR_EMPTY, COLOR_OUTLINE, COLOR_SELECTED

from Field import Field
from Snake import Snake


class FieldScene(object):
    def __init__(self, field: Field, canvasBlockSize: int, root: Tk, canvasField: Canvas):
        self._field = field
        self._canvasBlockSize = canvasBlockSize
        self._root = root
        self._canvasField = canvasField

        self._sceneData = [[None for h in range(
            self._field.height)] for w in range(self._field.width)]

        colorOutline = COLOR_OUTLINE.toHTMLColor
        for i in range(self._field.width):
            for j in range(self._field._height):
                self._sceneData[i][j] = self._drawRect(
                    canvasField, (i, j), self._field.getPointColorHTML((i, j)), colorOutline)

        self._field.setRedrawed()
        self._needRedraw = False
        self.setCaption()

    def _drawRect(self, canvasField: Canvas, p: tuple, fillColor, outlineColor):
        return canvasField.create_rectangle(p[0]*self._canvasBlockSize+1, p[1]*self._canvasBlockSize+1, (p[0]+1)*self._canvasBlockSize+1,
                                            (p[1]+1)*self._canvasBlockSize+1, fill=fillColor, outline=outlineColor)

    def save(self, name):
        img = Image.new(mode="RGB", size=(
            self._field.width, self._field.height), color=COLOR_EMPTY.toTuple)

        for i in range(self._field.width):
            for j in range(self._field._height):
                img.putpixel((i, j), self._sceneData[i][j])
        img.save(name)

    def drawAll(self):
        if self._field.needRedraw:
            sel = list() if Snake.selectedSnake is None else Snake.selectedSnake._body
            colorOutline = COLOR_OUTLINE.toHTMLColor
            colorSelected = COLOR_SELECTED.toHTMLColor

            for i in range(self._field.width):
                for j in range(self._field._height):
                    self._canvasField.itemconfigure(
                        self._sceneData[i][j], fill=self._field.getPointColorHTML((i, j)))
                    self._canvasField.itemconfigure(
                        self._sceneData[i][j], outline=(colorSelected if (i, j) in sel else colorOutline))
            self._field.setRedrawed()
            self._needRedraw = False
        self.setCaption()

    def setCaption(self):
        self._root.title(f"Field={self._field.width}x{self._field.height} Snakes={
            len(self._field.snakes)} Food={self._field.foodCount} Age={self._field.age}")

    def _pointToScreenRect(self, p) -> list:
        return (p[0]*self._canvasBlockSize, p[1]*self._canvasBlockSize,
                (p[0]+1)*self._canvasBlockSize, (p[1]+1)*self._canvasBlockSize)
