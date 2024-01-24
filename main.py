from datetime import datetime
import json
import time
import pygame as pg
from random import randint
from threading import Thread
from Enums.Direction import Direction
from Enums.MoveDirection import MoveDirection
from Color import COLOR_SNAKE_RANGE, Color
from SimpleNN import SimpleNN
from Snake import Snake
from Field import Field
#from Food import Food
from FieldScene import FieldScene

# pip freeze > requirements.txt
# pip install -r requirements.txt

FIELD_WIDTH = 70
FIELD_HEIGHT = 40

SNAKE_VIEW_RADIUS=2

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
SCREEN_FPS = 60

STEP_DELAY = 0.05

running: bool = True


def handle_events(fieldScene: FieldScene):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                return False
            if event.key == pg.K_HOME:
                fieldScene.left = 0
                fieldScene.top = 0

        if event.type != pg.MOUSEMOTION:
            # print(f"{draw_scene.left} {draw_scene.top}")
            pass

    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        fieldScene.left -= 1
    elif keys[pg.K_RIGHT]:
        fieldScene.left += 1
    elif keys[pg.K_UP]:
        fieldScene.top -= 1
    elif keys[pg.K_DOWN]:
        fieldScene.top += 1
    return True


def calculations(field: Field, fieldScene: FieldScene):
    global running
    while running and len(field.snakes) > 0:
        start = datetime.now()
        field.doOneStep()
        end = datetime.now()
        d = STEP_DELAY-(end - start).total_seconds()
        if d > 0:
            time.sleep(STEP_DELAY)
    fieldScene.drawAll()


def main():
    global running

    pg.init()
    disp = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()

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
    fieldScene = FieldScene(disp, field)

    th = Thread(name="calculation", target=calculations,                daemon=True, args=(field, fieldScene))
    th.start()

    while running:
        clock.tick(SCREEN_FPS)
        running = handle_events(fieldScene)
        fieldScene.drawAll()
        if len(field.snakes) == 0:
            running = False

    pg.quit()


if __name__ == '__main__':
    main()
