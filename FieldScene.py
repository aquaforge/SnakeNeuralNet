from tkinter import Tk, Canvas
from PIL import Image
from Color import COLOR_EMPTY, COLOR_FOOD, COLOR_OUTLINE, COLOR_SELECTED, COLOR_WALL

from Field import Field
from Snake import Snake


class FieldScene(object):
    def __init__(self, field: Field, canvasBlockSize: int, root: Tk, canvasField: Canvas,  canvasHead: Canvas):
        self._field = field
        self._canvasBlockSize = canvasBlockSize
        self._root = root
        self._canvasField = canvasField
        self._canvasHead = canvasHead

        self._canvasField.delete("all")
        self._canvasHead.delete("all")

        self._sceneData = [[None for h in range(
            self._field.height)] for w in range(self._field.width)]

        colorOutline = COLOR_OUTLINE.toHTMLColor
        for i in range(self._field.width):
            for j in range(self._field._height):
                self._sceneData[i][j] = self._drawRect(
                    canvasField, (i, j), self._canvasBlockSize, self._field.getPointColorHTML((i, j)), colorOutline)

        self._field.setRedrawed()
        self._needRedraw = False
        self.setCaption()

    def _drawRect(self, canvasField: Canvas, p: tuple, blockSize: int, fillColor, outlineColor):
        return canvasField.create_rectangle(p[0]*blockSize+1, p[1]*blockSize+1, (p[0]+1)*blockSize+1,
                                            (p[1]+1)*blockSize+1, fill=fillColor, outline=outlineColor)

    def save(self, name):
        img = Image.new(mode="RGB", size=(
            self._field.width, self._field.height), color=COLOR_EMPTY.toTuple)

        for i in range(self._field.width):
            for j in range(self._field._height):
                img.putpixel((i, j), self._sceneData[i][j])
        img.save(name)

    def drawAll(self):
        if self._field.needRedraw:
            sel = list() if self._field.selectedSnake is None else self._field.selectedSnake._body
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
            self._drawSnakeView()
        self.setCaption()

    def setCaption(self):
        self._root.title(f"Field={self._field.width}x{self._field.height} Snakes={
            len(self._field.snakes)} Food={self._field.foodCount} Age={self._field.age}")

    def _pointToScreenRect(self, p) -> list:
        return (p[0]*self._canvasBlockSize, p[1]*self._canvasBlockSize,
                (p[0]+1)*self._canvasBlockSize, (p[1]+1)*self._canvasBlockSize)

    def _drawSnakeView(self):
        self._canvasHead.delete("all")
        if self._field.selectedSnake is not None:
            snake =  self._field.selectedSnake
            view = snake.getHeadView(self._field.getPointType)

            colorEmpty = COLOR_EMPTY.toHTMLColor
            arrayDim = 2*snake.viewRadius+1
            blockSize = 15
            self._canvasHead.place(
                width=blockSize*arrayDim, height=blockSize*arrayDim)
            for i in range(arrayDim):
                for j in range(arrayDim):
                    col = COLOR_EMPTY.toHTMLColor
                    if i == snake.viewRadius and j == snake.viewRadius:
                        col = "#BBBBBB"
                    elif view[i, j] == 1:
                        col = COLOR_FOOD.toHTMLColor
                    elif view[i, j] == -1:
                        col = COLOR_WALL.toHTMLColor
                    self._drawRect(self._canvasHead, (i, j),
                                   blockSize, col, colorEmpty)
