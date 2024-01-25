from datetime import datetime
import json
import time
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk
from random import randint
from threading import Thread
from Enums.Direction import Direction
from Enums.MoveDirection import MoveDirection
from Color import COLOR_SNAKE_RANGE, Color
from SimpleNN import SimpleNN
from Snake import Snake
from Field import Field
# from Food import Food
from FieldScene import FieldScene

# pip freeze > requirements.txt
# pip install -r requirements.txt

FIELD_WIDTH = 70
FIELD_HEIGHT = 40

SNAKE_VIEW_RADIUS = 2

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
CANVAS_BLOCK_SIZE = 15


STEP_DELAY = 0.05

running: bool = True


def calculations(root: Tk, field: Field, fieldScene: FieldScene):
    global running
    if len(field.snakes) == 0:
        running = False
    else:
        start = datetime.now()
        field.doOneStep()
        end = datetime.now()
        d = STEP_DELAY-(end - start).total_seconds()
        if d > 0:
            pass  # time.sleep(STEP_DELAY)
        fieldScene.drawAll()

    if running:
        root.after(100, calculations, root, field, fieldScene)


def main():
    global running

    root = Tk()
    root.geometry("1000x800+100+100")

    frameLeft = ttk.Frame(master=root, borderwidth=1,
                          padding=10, relief=SOLID, width=300)
    frameLeft.pack(side=LEFT, fill=Y, padx=2, pady=2)
    label = ttk.Label(frameLeft, text="frameLeft")
    label.pack(anchor=NW)

    frameRight = ttk.Frame(master=root, borderwidth=1, relief=SOLID)
    frameRight.pack(fill=BOTH, expand=True,  padx=2, pady=2)

    v = ttk.Scrollbar(master=frameRight, orient=VERTICAL)
    h = ttk.Scrollbar(master=frameRight, orient=HORIZONTAL)

    canvasField = Canvas(master=frameRight, scrollregion=(0, 0, FIELD_WIDTH*CANVAS_BLOCK_SIZE, 
                                                          FIELD_HEIGHT*CANVAS_BLOCK_SIZE),
                         bg="white", yscrollcommand=v.set, xscrollcommand=h.set)
    h["command"] = canvasField.xview
    v["command"] = canvasField.yview

    canvasField.grid(column=0, row=0, sticky=(N, W, E, S))
    h.grid(column=0, row=1, sticky=(W, E))
    v.grid(column=1, row=0, sticky=(N, S))
    frameRight.grid_columnconfigure(0, weight=1)
    frameRight.grid_rowconfigure(0, weight=1)

    field = Field(FIELD_WIDTH, FIELD_HEIGHT)

    h = 2
    while h+7 < FIELD_HEIGHT:
        w = 2
        while w+3 < FIELD_WIDTH:
            # здоровье+длина + массив (2*SNAKE_VIEW_RADIUS+1)^2 для взгляда заятно\пусто\еда
            model = SimpleNN((2*SNAKE_VIEW_RADIUS+1)**2)
            model.add(10, activation="relu", use_bias=True)
            # model.add(len(MoveDirection)+1, activation="relu", use_bias=False)
            model.add(len(MoveDirection), activation="softmax")

            field.snakes.add(Snake([(w, h+k) for k in range(5)], SNAKE_VIEW_RADIUS, model, Direction.LEFT,
                                   Color.randomColor(COLOR_SNAKE_RANGE[0], COLOR_SNAKE_RANGE[1])))
            w += 3
        h += 7

    field.addFood()
    fieldScene = FieldScene(field, CANVAS_BLOCK_SIZE, root, canvasField)

    # th = Thread(name="calculation", target=calculations,                daemon=True, args=(field, fieldScene))
    # th.start()

    fieldScene.drawAll()
    root.after(100, calculations, root, field, fieldScene)

    root.update_idletasks()
    root.mainloop()
    running = False

    '''
    while running:
        clock.tick(SCREEN_FPS)
        running = handle_events(fieldScene)
        fieldScene.drawAll()
        if len(field.snakes) == 0:
            running = False

    pg.quit()
    '''


if __name__ == '__main__':
    main()
