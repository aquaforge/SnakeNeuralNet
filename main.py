from datetime import datetime
import json
import time
import pygame as pg
from random import randint
from threading import Thread
from Enums.Direction import Direction
from Enums.MoveDirection import MoveDirection

from Enums.Point2D import Point2D
from SimpleNN import SimpleNN
from DrawScene import DrawScene
from Color import Color
from Field import Field
from Snake import Snake, SNAKE_VIEW_RADIUS

# pip freeze > requirements.txt
# pip install -r requirements.txt

FIELD_WIDTH = 130
FIELD_HEIGHT = 70

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
SCREEN_FPS = 60
SCREEN_BLOCK_SIZE = 10
SCREEN_BLOCK_MARGIN = 1
SCREEN_BORDER_MARGIN = 5

STEP_DELAY = 0.05

running: bool = True


def handle_events(drawScene: DrawScene):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                return False
            if event.key == pg.K_HOME:
                drawScene.left = 0
                drawScene.top = 0

        if event.type != pg.MOUSEMOTION:
            # print(f"{draw_scene.left} {draw_scene.top}")
            pass

    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        drawScene.left -= 1
    elif keys[pg.K_RIGHT]:
        drawScene.left += 1
    elif keys[pg.K_UP]:
        drawScene.top -= 1
    elif keys[pg.K_DOWN]:
        drawScene.top += 1

    return True


def calculations(field: Field):
    global running
    while running and field.snakeCount > 0:
        start = datetime.now()
        field.do_one_step()
        end = datetime.now()
        d = STEP_DELAY-(end - start).total_seconds()
        if d > 0:
            time.sleep(STEP_DELAY)
    field.getMatrixColor(True)


def main():
    global running

    pg.init()
    sc = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption(f"Field: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    clock = pg.time.Clock()

    snakes = set()
    food = set()

    h = 5
    while h+8 < FIELD_HEIGHT:
        w = 5
        while w+5 < FIELD_WIDTH:
            #food.add(Point2D(h, w))

            # здоровье+длина + массив (2*SNAKE_VIEW_RADIUS+1)^2 для взгляда заятно\пусто\еда
            model = SimpleNN(2+(2*SNAKE_VIEW_RADIUS+1)**2)
            model.add(10, activation="relu", use_bias=True)
            # model.add(len(MoveDirection)+1, activation="relu", use_bias=False)
            model.add(len(MoveDirection), activation="softmax")

            body = [Point2D(h+2+k, w) for k in range(5)]
            snakes.add(Snake(body, model, Direction.LEFT,
                       Color.random(100, 200), 100.0))
            w += 3
        h += 20

    field = Field(FIELD_WIDTH, FIELD_HEIGHT, snakes,
                  food, 0.05 * FIELD_WIDTH * FIELD_HEIGHT)
    drawScene = DrawScene(sc, field, SCREEN_BLOCK_SIZE,
                          SCREEN_BLOCK_MARGIN, SCREEN_BORDER_MARGIN)

    th = Thread(name="calculation", target=calculations,
                daemon=True, args=(field,))
    th.start()

    while running:
        clock.tick(SCREEN_FPS)
        running = handle_events(drawScene)
        drawScene.draw()
        if field.snakeCount==0:
            running=False

    pg.quit()


if __name__ == '__main__':
    main()
