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
CANVAS_BLOCK_SIZE = 10


STEP_DELAY_MS = 100

running: bool = True


def calculations(root: Tk, field: Field, fieldScene: FieldScene):
    global running
    if running and len(field.snakes) == 0:
        running = False
    else:
        start = datetime.now()
        field.doOneStep()
        end = datetime.now()
        d = int(STEP_DELAY_MS-1000*(end - start).total_seconds())
        print(d)
        fieldScene.drawAll()
        root.after(d if d > 0 else STEP_DELAY_MS,
                   calculations, root, field, fieldScene)
    # _imgPILField = Image.new(mode="RGB", size=(
    #     FIELD_WIDTH*CANVAS_BLOCK_SIZE, FIELD_HEIGHT*CANVAS_BLOCK_SIZE), color=(200, 250, 200))
    # _drawPILField = ImageDraw.Draw(_imgPILField)

    # _drawPILField.rectangle(
    #     xy=(10, 10, 100, 100), fill=250, outline=100, width=1)
    # _imgPILField.save("a1.png")

    # t = ImageTk.PhotoImage(_imgPILField)
    # fieldScene._canvasField.create_image(
    #     0, 0, anchor=NW, image=t)


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
                         bg="green", yscrollcommand=v.set, xscrollcommand=h.set)
    h["command"] = canvasField.xview
    v["command"] = canvasField.yview

    canvasField.grid(column=0, row=0, sticky=(N, W, E, S))
    h.grid(column=0, row=1, sticky=(W, E))
    v.grid(column=1, row=0, sticky=(N, S))
    frameRight.grid_columnconfigure(0, weight=1)
    frameRight.grid_rowconfigure(0, weight=1)


    ## https://gist.github.com/PM2Ring/d7878c904df8da838f76dc4a15c6c746

    # img = Image.new(mode="RGB", size=(
    #      FIELD_WIDTH*CANVAS_BLOCK_SIZE,FIELD_HEIGHT*CANVAS_BLOCK_SIZE), color=(220, 220, 220))
    # draw = ImageDraw.Draw(img)
    # # draw.line((0, 0) + img.size, fill=220)
    # # draw.line((0, im.size[1], im.size[0], 0), fill=128)
    # # PIL.Image.putpixel(xy, value)
    # for i in range(0, 10):
    #     for j in range(0, 15):
    #         draw.rectangle(             xy=(10,10,100,100), fill=250, outline=100, width=1)
    # # draw.rectangle([(10, 10), (50, 50)], fill=(        255, 0, 0), outline=(0, 0, 0), width=1)
    # t = ImageTk.PhotoImage(img)
    # canvasField.create_image(0, 0, anchor=NW, image=t)

    field = Field(FIELD_WIDTH, FIELD_HEIGHT)

    h = 2
    while h+7 < FIELD_HEIGHT:
        w = 2
        while w+3 < FIELD_WIDTH:
            # здоровье+длина + массив (2*SNAKE_VIEW_RADIUS+1)^2 для взгляда занято\пусто\еда
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
