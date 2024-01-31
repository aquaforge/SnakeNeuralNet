from datetime import datetime
from random import Random, randint, random
from tkinter import *
from tkinter import ttk
from Brains.BrainBase import BrainBase
from Brains.BrainPathFind import BrainPathFind
from Brains.BrainSimpleNN import BrainSimpleNN
from DbSnakeData import DbSnakeData
from SimpleNN import SimpleNN
from Enums.Direction import Direction
from Color import COLOR_EMPTY, COLOR_SNAKE_RANGE, Color
from Snake import Snake
from Field import Field
from FieldScene import FieldScene
from DbTrainData import TrainData, DbTrainData


# pip freeze > requirements.txt
# pip install -r requirements.txt
# https://metanit.com/python/database/3.1.php

# https://ru.hexlet.io/blog/posts/19-bibliotek-dlya-python?ysclid=lrus9b9ejh622626382

FIELD_WIDTH = 102*2
FIELD_HEIGHT = 57*2
CANVAS_BLOCK_SIZE = 8 #15

# FIELD_WIDTH = 102
# FIELD_HEIGHT = 57
# CANVAS_BLOCK_SIZE = 15


SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 900
STEP_DELAY_MS = 10

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
    viewRadius = 8  # randint(4, 9)

    if True:
        snakesBestData = DbSnakeData().getBestTop(5000)
    else:
        snakesBestData = None

    h = 2
    while h+15 < FIELD_HEIGHT:
        w = 2
        while w+5 < FIELD_WIDTH:
            if snakesBestData is not None and len(snakesBestData) > 0:
                col = Color(randint(70, 230), randint(
                    70, 230), randint(70, 230))
                snakeData = snakesBestData[randint(0, len(snakesBestData)-1)]
                nn = SimpleNN.decode(snakeData['data'])
                nn._id = snakeData['id']
                field.addSnakeToField(Snake([(w, h+k) for k in range(7)],  BrainSimpleNN(
                    snakeData["viewRadius"], nn, mse=snakeData["mse"]), Direction.UP, col))
            else:
                viewRadius = randint(1, 15)
                col = Color(0, randint(150, 200), 0)
                field.addSnakeToField(Snake([(w, h+k) for k in range(5)],  BrainPathFind(
                    viewRadius), Direction.UP, col))
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

---------------Path find snake algorythm: eatCount/age % by viewRadius------------------------------------------------------
FIELD_WIDTH = 100
FIELD_HEIGHT = 50
self._maxFoodCount = int(0.01 * width * height)
epoch=1 DB=48564 2="4.6"  3="6.0"  4="7.0"  5="6.97"  6="8.1"  7="7.55"  8="9.0"  9="7.5"  10="7.74"  11="9.55"  12="8.93"
epoch=2 DB=96979 2="5.0"  3="5.05"  4="6.4"  5="6.25"  6="7.6"  7="7.71"  8="7.42"  9="8.78"  10="7.77"  11="8.58"  12="8.93"
epoch=3 DB=142204 2="5.07"  3="5.1"  4="6.1"  5="7.83"  6="7.23"  7="8.07"  8="7.78"  9="8.47"  10="8.15"  11="8.47"  12="9.1"
epoch=4 DB=188593 2="5.0"  3="5.25"  4="5.88"  5="7.96"  6="7.88"  7="7.82"  8="8.18"  9="8.44"  10="8.08"  11="8.25"  12="9.12"
epoch=5 DB=235409 2="5.23"  3="5.37"  4="6.06"  5="7.47"  6="8.15"  7="7.9"  8="7.81"  9="7.33"  10="8.7"  11="8.15"  12="9.07"
epoch=6 DB=282210 2="5.4"  3="5.33"  4="6.33"  5="6.03"  6="7.73"  7="8.05"  8="8.05"  9="8.47"  10="9.63"  11="8.6"  12="8.62"
epoch=7 DB=330265 2="4.7"  3="5.1"  4="6.55"  5="6.5"  6="8.55"  7="7.93"  8="7.86"  9="7.7"  10="9.17"  11="8.77"  12="8.59"
epoch=8 DB=378860 3="5.3"  4="6.42"  5="7.25"  6="8.04"  7="7.57"  8="8.12"  9="7.7"  10="8.62"  11="8.35"  12="9.03"
epoch=9 DB=423642 3="5.57"  4="5.92"  5="6.82"  6="8.7"  7="7.78"  8="8.7"  9="7.8"  10="9.03"  11="8.93"  12="8.42"
epoch=10 DB=465159 2="5.25"  3="6.47"  4="6.65"  5="6.97"  6="7.38"  7="8.23"  8="7.24"  9="8.74"  10="9.52"  11="8.26"  12="9.12"
epoch=11 DB=513604 2="5.95"  3="4.98"  4="6.72"  5="7.64"  6="6.77"  7="7.43"  8="7.0"  9="8.3"  10="9.02"  11="9.12"  12="8.7"
epoch=12 DB=565054 3="6.1"  4="6.8"  5="6.78"  6="7.88"  7="6.67"  8="7.76"  9="7.87"  10="8.34"  11="8.93"  12="8.66"
epoch=13 DB=609190 2="5.07"  3="5.67"  4="6.7"  5="6.5"  6="6.7"  7="7.95"  8="7.6"  9="8.22"  10="7.3"  11="9.26"  12="8.5"
epoch=14 DB=656221 2="4.7"  3="5.6"  4="6.83"  5="7.42"  6="7.47"  7="8.0"  8="7.9"  9="8.94"  10="8.64"  11="8.79"  12="9.15"
epoch=15 DB=706210 3="6.6"  4="7.24"  5="6.58"  6="7.4"  7="7.7"  8="7.95"  9="7.52"  10="8.46"  11="7.38"  12="9.45"
epoch=16 DB=752046 2="5.75"  3="5.95"  4="5.65"  5="6.97"  6="8.58"  7="8.07"  8="7.77"  9="9.6"  10="8.81"  11="8.96"  12="8.78"
epoch=17 DB=794143 2="4.8"  3="5.78"  4="4.5"  5="6.61"  6="8.68"  7="7.1"  8="7.8"  9="9.23"  10="8.44"  11="8.34"  12="9.4"
epoch=18 DB=839777 2="4.95"  3="5.72"  4="6.45"  5="6.85"  6="6.15"  7="7.98"  8="7.98"  9="8.73"  10="7.76"  11="8.07"  12="9.8"
epoch=19 DB=884453 2="4.68"  4="6.36"  5="6.8"  6="7.8"  7="7.85"  8="6.47"  9="8.98"  10="8.47"  11="8.8"  12="9.28"
epoch=20 DB=933092 2="5.1"  3="6.53"  4="6.5"  5="7.4"  6="7.12"  7="8.46"  8="7.49"  9="8.3"  10="8.3"  11="7.96"  12="8.87"
epoch=21 DB=980015 2="5.23"  3="5.57"  4="6.9"  5="7.04"  6="8.1"  7="9.03"  8="8.8"  9="8.27"  10="9.52"  11="9.22"  12="8.3"
epoch=22 DB=1026821 2="4.8"  3="5.22"  4="5.95"  5="7.7"  6="7.52"  7="7.3"  8="8.22"  9="8.47"  10="9.43"  11="8.88"  12="9.5"
epoch=23 DB=1073961 2="5.2"  3="5.9"  4="5.7"  5="6.88"  6="8.75"  7="8.12"  8="9.12"  9="9.17"  10="8.45"  11="7.71"  12="9.21"
epoch=24 DB=1124153 3="5.64"  4="7.47"  5="7.31"  6="7.7"  7="7.48"  8="7.65"  9="7.28"  10="8.44"  11="8.86"  12="8.4"
epoch=25 DB=1170695 3="5.12"  4="6.23"  5="7.54"  6="7.38"  7="6.0"  8="8.3"  9="9.23"  10="8.34"  11="9.45"  12="7.84"
epoch=26 DB=1217498 2="4.5"  3="6.5"  4="6.63"  5="7.14"  6="7.45"  7="7.81"  8="8.15"  9="8.92"  10="8.8"  11="8.66"  12="8.13"
epoch=27 DB=1261645 3="5.0"  4="6.54"  5="5.63"  6="7.1"  7="8.18"  8="9.2"  9="8.57"  10="9.0"  11="8.54"  12="7.63"
epoch=28 DB=1309356 2="5.3"  3="5.47"  4="5.6"  5="7.7"  6="7.45"  7="8.25"  8="7.61"  9="8.28"  10="7.75"  11="8.61"  12="8.7"
epoch=29 DB=1352052 2="4.47"  3="5.46"  4="7.37"  5="7.38"  6="7.12"  7="6.43"  8="9.3"  9="7.78"  10="8.66"  11="7.83"  12="9.52"
epoch=30 DB=1397474 2="5.07"  3="5.49"  4="5.8"  5="7.22"  6="8.0"  7="8.28"  8="7.1"  9="8.8"  10="9.53"  11="8.86"  12="8.12"
'''


def calculateOne(root: Tk, canvasField: Canvas,  canvasHead: Canvas, snakeInfo: Text):
    global running
    global field
    global fieldScene
    global paused
    global epochCount


    if not running:
        return

    if len(field.snakes) == 0 or field.age >= 1000:
        dbo = DbTrainData()
        countDB = dbo.countTable(TrainData)

        dbo = None
        print(f"epoch={epochCount}", f"DB={countDB}", " ".join(
            [f"{k}=\"{v}\"" for k, v in field.getAverageRank()]))
        field._saveToDB()
        for snake in field.snakes:
            snake._saveInfo()

        initializeAll(root, canvasField,  canvasHead, snakeInfo)
    else:
        start = datetime.now()
        if not paused:
            field.doOneStep()


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

    snakeInfo = Text(master=frameLeft, width=25, height=8, wrap="word")
    # snakeInfo.pack(anchor=NW)
    snakeInfo.grid(row=1, column=1)

    view_radius = 10
    canvasHead = Canvas(master=frameLeft, width=200,
                        height=200, bg=COLOR_EMPTY.toHTMLColor)
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
