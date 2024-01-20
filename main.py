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
from Snake import Snake

# pip freeze > requirements.txt
# pip install -r requirements.txt

FIELD_WIDTH = 128
FIELD_HEIGHT = 97

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
SCREEN_FPS = 60
SCREEN_BLOCK_SIZE = 8
SCREEN_BLOCK_MARGIN = 1
SCREEN_BORDER_MARGIN = 5

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
        field.do_one_step()
    field.getMatrixColor(True)


def main():
    global running

    pg.init()
    sc = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption(f"Field: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    clock = pg.time.Clock()

    snakes = set()
    for i in range(60):
        model = SimpleNN(1+2*3*3)
        model.add(10, activation="relu", use_bias=True)
        model.add(len(MoveDirection)+1, activation="relu", use_bias=False)
        model.add(len(MoveDirection), activation="softmax")

        body = [Point2D(30+k, 5+i*2) for k in range(10)]
        snakes.add(Snake(body, model,
                   Direction.UP, Color.random(100, 200), 100.0))

    food = set()
    for i in range(60):
        food.add(Point2D(10, 5+i*2))

    field = Field(FIELD_WIDTH, FIELD_HEIGHT, snakes, food, 100)
    drawScene = DrawScene(sc, field, SCREEN_BLOCK_SIZE,
                          SCREEN_BLOCK_MARGIN, SCREEN_BORDER_MARGIN)

    th = Thread(name="calculation", target=calculations,
                daemon=True, args=(field,))
    th.start()

    while running:
        clock.tick(SCREEN_FPS)
        running = handle_events(drawScene)
        drawScene.draw()
    pg.quit()


if __name__ == '__main__':
    main()
