from datetime import datetime
from random import Random, randint
from tkinter import *
from tkinter import ttk
from Brains.BrainBase import BrainBase
from Brains.BrainPathFind import BrainPathFind
from Brains.BrainSimpleNN import BrainSimpleNN
from SimpleNN import SimpleNN
from Enums.Direction import Direction
from Color import COLOR_EMPTY, COLOR_SNAKE_RANGE, Color
from Snake import Snake
from Field import Field
from FieldScene import FieldScene
from dbPathData import DbPathData, PathDataInfo

# pip freeze > requirements.txt
# pip install -r requirements.txt
# https://metanit.com/python/database/3.1.php

# https://ru.hexlet.io/blog/posts/19-bibliotek-dlya-python?ysclid=lrus9b9ejh622626382

FIELD_WIDTH = 100
FIELD_HEIGHT = 50
CANVAS_BLOCK_SIZE = 15

# FIELD_WIDTH = 500
# FIELD_HEIGHT = 100
# CANVAS_BLOCK_SIZE = 10


# SNAKE_VIEW_RADIUS = 3

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 900

STEP_DELAY_MS = 100

running: bool = True
paused: bool = False
field = None
fieldScene = None
epochCount = 0


def initializeAll(root: Tk, canvasField: Canvas,  canvasHead: Canvas, snakeInfo: Text):
    global running
    global field
    global fieldScene
    global paused
    global epochCount

    epochCount += 1

    field = Field(FIELD_WIDTH, FIELD_HEIGHT)
    h = 2
    while h+15 < FIELD_HEIGHT:
        w = 2
        while w+5 < FIELD_WIDTH:
            # # здоровье+длина + массив (2*SNAKE_VIEW_RADIUS+1)^2 для взгляда занято\пусто\еда
            # model = SimpleNN((2*SNAKE_VIEW_RADIUS+1)**2)
            # model.add(10, activation="relu", use_bias=True)
            # # model.add(len(MoveDirection)+1, activation="relu", use_bias=False)
            # model.add(len(MoveDirection), activation="softmax")

            # field.addSnakeToField(Snake([(w, h+k) for k in range(7)], BrainSimpleNN(SNAKE_VIEW_RADIUS, model), Direction.UP,
            #                             Color.randomColor(COLOR_SNAKE_RANGE[0], COLOR_SNAKE_RANGE[1])))

            # field.addSnakeToField(Snake([(w, h+k) for k in range(7)], BrainBase(SNAKE_VIEW_RADIUS), Direction.UP,
            #                             Color.randomColor(COLOR_SNAKE_RANGE[0], COLOR_SNAKE_RANGE[1])))

            field.addSnakeToField(Snake([(w, h+k) for k in range(7)], BrainPathFind(randint(2, 10)), Direction.UP,
                                        Color.randomColor(COLOR_SNAKE_RANGE[0], COLOR_SNAKE_RANGE[1])))

            # col = randint(COLOR_SNAKE_RANGE[0], COLOR_SNAKE_RANGE[1])
            # field.addSnakeToField(Snake(body=[(w, h+k) for k in range(7)],
            #                             brain=BrainPathFind(randint(2, 10)),
            #                             headViewDirection=Direction.UP,
            #                             color=Color(COLOR_SNAKE_RANGE[0], COLOR_SNAKE_RANGE[0],col)))
            w += 5
        h += 15

    field.addFood()
    fieldScene = FieldScene(field, CANVAS_BLOCK_SIZE,
                            root, canvasField, canvasHead, snakeInfo)

    fieldScene.drawAll()
    root.after(500, calculateOne, root, canvasField,  canvasHead, snakeInfo)


'''
запускать разного цвета
 - часть обученных змеек с поиском пути
 - часть обученных змеек с нейронкой (НС) из подготовленного списка или быстро обучить как-то или рандомно
сохранять 
- данные для обучения
- обученные НС с snake.age + eatCount (totalAge, eatCount)

---------------Path find snake algorythm---------------------------------------------------------
FIELD_WIDTH = 100
FIELD_HEIGHT = 50
self._maxFoodCount = int(0.01 * width * height)
epoch=1 DB=2419390 2="5.26"  3="4.99"  4="6.94"  5="6.64"  6="7.39"  7="7.54"  8="8.27"  9="8.88"
epoch=2 DB=2441064 2="3.99"  3="4.95"  4="6.12"  5="7.23"  6="6.39"  7="7.61"  8="7.98"  9="8.18"
epoch=3 DB=2462134 2="4.55"  3="6.09"  4="5.55"  5="6.51"  6="6.79"  7="8.28"  8="8.21"  9="8.68"
epoch=4 DB=2483659 2="4.97"  3="4.19"  4="6.72"  5="7.07"  6="7.35"  7="9.18"  8="9.06"  9="7.71"
epoch=5 DB=2505669 2="4.39"  3="5.91"  4="5.39"  5="7.5"  6="7.75"  7="7.65"  8="8.86"  9="8.07"
epoch=6 DB=2525179 2="4.9"  3="5.82"  4="6.16"  5="5.79"  6="7.35"  7="9.34"  8="8.9"  9="7.73"
epoch=7 DB=2545498 2="4.43"  3="4.92"  4="6.7"  5="7.11"  6="8.89"  7="8.35"  8="8.58"  9="8.75"
epoch=8 DB=2568004 2="5.07"  3="5.52"  4="6.89"  5="6.95"  6="8.18"  7="8.46"  8="8.38"  9="7.75"
epoch=9 DB=2589603 2="3.93"  3="4.79"  4="5.63"  5="7.29"  6="8.73"  7="8.52"  8="9.18"  9="7.66"
epoch=10 DB=2611547 2="4.59"  3="4.93"  4="6.83"  5="7.14"  6="7.63"  7="8.05"  8="6.71"  9="7.78"
epoch=11 DB=2631815 2="4.64"  3="5.95"  4="6.87"  5="6.29"  6="8.12"  7="7.49"  8="9.27"  9="8.41"
epoch=12 DB=2653124 2="4.39"  3="5.79"  4="6.25"  5="7.34"  6="7.5"  7="7.73"  8="7.83"  9="8.88"
epoch=13 DB=2674632 2="4.46"  3="5.59"  4="6.61"  5="6.83"  6="7.58"  7="8.07"  8="6.99"  9="8.52"
epoch=14 DB=2696042 2="4.46"  3="5.26"  4="5.9"  5="7.44"  6="8.41"  7="8.38"  8="7.7"  9="9.58"
epoch=15 DB=2718450 2="5.19"  3="6.01"  4="6.13"  5="6.59"  6="7.44"  7="8.78"  8="8.28"  9="9.51"
epoch=16 DB=2739077 2="3.84"  3="4.79"  4="6.52"  5="6.15"  6="7.83"  7="7.19"  8="8.25"  9="8.65"
epoch=17 DB=2759607 2="4.96"  3="5.9"  4="5.85"  5="7.39"  6="7.06"  7="8.72"  8="8.14"  9="8.85"
epoch=18 DB=2781319 2="4.96"  3="6.66"  4="6.94"  5="6.75"  6="7.39"  7="7.41"  8="9.18"  9="8.83"
epoch=19 DB=2802119 2="4.06"  3="5.16"  4="6.69"  5="7.78"  6="6.99"  7="9.18"  8="8.35"  9="8.03"
epoch=20 DB=2821645 2="4.69"  3="5.06"  4="4.66"  5="7.12"  6="6.67"  7="9.28"  8="9.35"  9="9.12"

'''


def calculateOne(root: Tk, canvasField: Canvas,  canvasHead: Canvas, snakeInfo: Text):
    global running
    global field
    global fieldScene
    global paused
    global epochCount

    if not running:
        return
    if len(field.snakes) == 0 or field.age > 500:
        dbo = DbPathData()
        countDB = dbo.countTable(PathDataInfo)
        dbo = None
        # pathfind 3="5.49"  4="6.59"  5="6.69"  6="7.81"  7="8.83"  8="7.19"  9="7.29"
        print(f"epoch={epochCount}", f"DB={countDB}", "  ".join(
            [f"{k}=\"{v}\"" for k, v in field.getAverageRank()]))
        initializeAll(root, canvasField,  canvasHead, snakeInfo)
    else:
        start = datetime.now()
        if not paused:
            field.doOneStep()
            # fieldScene.saveImage("aa.png")
        fieldScene.drawAll()
        end = datetime.now()
        d = int(STEP_DELAY_MS-1000*(end - start).total_seconds())
        # print(d)
        root.after(d if d > 0 else STEP_DELAY_MS, calculateOne,
                   root, canvasField,  canvasHead, snakeInfo)


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
    root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}+10+10")

    frameLeft = ttk.Frame(master=root, borderwidth=1,
                          padding=10, relief=SOLID, width=300)
    frameLeft.pack(side=LEFT, fill=Y, padx=2, pady=2)

    snakeInfo = Text(master=frameLeft, width=30, height=8, wrap="word")
    # snakeInfo.pack(anchor=NW)
    snakeInfo.grid(row=1, column=1)

    view_radius = 10
    canvasHead = Canvas(master=frameLeft, width=(2*view_radius+1)*15,
                        height=(2*view_radius+1)*15, bg=COLOR_EMPTY.toHTMLColor)
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

    initializeAll(root, canvasField,  canvasHead, snakeInfo)

    root.update_idletasks()
    root.mainloop()
    running = False


if __name__ == '__main__':
    main()
