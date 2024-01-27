from datetime import datetime
import json
import time
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk
from random import randint
from threading import Thread
from BrainSimpleNN import BrainSimpleNN
from Enums.Direction import Direction
from Enums.MoveDirection import MoveDirection
from Color import COLOR_EMPTY, COLOR_SNAKE_RANGE, Color
from SimpleNN import SimpleNN
from Snake import Snake
from Field import Field
# from Food import Food
from FieldScene import FieldScene

# pip freeze > requirements.txt
# pip install -r requirements.txt

# https://ru.hexlet.io/blog/posts/19-bibliotek-dlya-python?ysclid=lrus9b9ejh622626382

FIELD_WIDTH = 50
FIELD_HEIGHT = 35
CANVAS_BLOCK_SIZE = 15

SNAKE_VIEW_RADIUS = 2

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

STEP_DELAY_MS = 100

running: bool = True
paused: bool = False
field = None


def calculations(root: Tk, field: Field, fieldScene: FieldScene):
    global running
    if running and len(field.snakes) == 0:
        running = False
    else:
        start = datetime.now()
        if not paused:
            field.doOneStep()
        end = datetime.now()
        d = int(STEP_DELAY_MS-1000*(end - start).total_seconds())
        # print(d)
        fieldScene.drawAll()
        root.after(d if d > 0 else STEP_DELAY_MS,
                   calculations, root, field, fieldScene)


def onWindowKeyPress(e):
    global paused
    # print ("pressed", repr(e.char))
    if e.char == ' ':
        paused = not paused


def onCanvasFieldClick(e):
    p = (e.x//CANVAS_BLOCK_SIZE, e.y//CANVAS_BLOCK_SIZE)
    field.selectSnakeByPoint(p)


def main():
    global running
    global field

    root = Tk()
    root.bind('<Key>', onWindowKeyPress)
    root.geometry("1000x800+100+100")

    frameLeft = ttk.Frame(master=root, borderwidth=1,
                          padding=10, relief=SOLID, width=300)
    frameLeft.pack(side=LEFT, fill=Y, padx=2, pady=2)

    snakeInfo = Text(master=frameLeft, width=15, height=5, wrap="word")
    # snakeInfo.pack(anchor=NW)
    snakeInfo.grid(row=1, column=1)

    canvasHead = Canvas(master=frameLeft, width=(2*SNAKE_VIEW_RADIUS+1)*15,
                        height=(2*SNAKE_VIEW_RADIUS+1)*15, bg=COLOR_EMPTY.toHTMLColor)
    # canvasHead.pack(anchor=NW)
    canvasHead.grid(row=2, column=1)

    frameLeft.grid_columnconfigure(0, weight=1)
    frameLeft.grid_rowconfigure(0, weight=1)    

    frameRight = ttk.Frame(master=root, borderwidth=1, relief=SOLID)
    frameRight.pack(fill=BOTH, expand=True,  padx=2, pady=2)

    v = ttk.Scrollbar(master=frameRight, orient=VERTICAL)
    h = ttk.Scrollbar(master=frameRight, orient=HORIZONTAL)

    canvasField = Canvas(master=frameRight, scrollregion=(0, 0, FIELD_WIDTH*CANVAS_BLOCK_SIZE,
                                                          FIELD_HEIGHT*CANVAS_BLOCK_SIZE),
                         bg=COLOR_EMPTY.toHTMLColor, yscrollcommand=v.set, xscrollcommand=h.set)
    h["command"] = canvasField.xview
    v["command"] = canvasField.yview

    canvasField.grid(column=0, row=0, sticky=(N, W, E, S))
    h.grid(column=0, row=1, sticky=(W, E))
    v.grid(column=1, row=0, sticky=(N, S))
    frameRight.grid_columnconfigure(0, weight=1)
    frameRight.grid_rowconfigure(0, weight=1)
    canvasField.bind("<Button-1>", onCanvasFieldClick)

    field = Field(FIELD_WIDTH, FIELD_HEIGHT)

    h = 2
    while h+15 < FIELD_HEIGHT:
        w = 2
        while w+5 < FIELD_WIDTH:
            # здоровье+длина + массив (2*SNAKE_VIEW_RADIUS+1)^2 для взгляда занято\пусто\еда
            model = SimpleNN((2*SNAKE_VIEW_RADIUS+1)**2)
            model.add(10, activation="relu", use_bias=True)
            # model.add(len(MoveDirection)+1, activation="relu", use_bias=False)
            model.add(len(MoveDirection), activation="softmax")

            field.addSnakeToField(Snake([(w, h+k) for k in range(7)], BrainSimpleNN(SNAKE_VIEW_RADIUS, model), Direction.UP,
                                        Color.randomColor(COLOR_SNAKE_RANGE[0], COLOR_SNAKE_RANGE[1])))
            w += 5
        h += 15

    field.addFood()
    fieldScene = FieldScene(field, CANVAS_BLOCK_SIZE,
                            root, canvasField, canvasHead, snakeInfo)

    # th = Thread(name="calculation", target=calculations,                daemon=True, args=(field, fieldScene))
    # th.start()

    fieldScene.drawAll()
    root.after(100, calculations, root, field, fieldScene)

    root.update_idletasks()
    root.mainloop()
    running = False


if __name__ == '__main__':
    main()
