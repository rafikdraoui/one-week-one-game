#!/usr/bin/env python

from collections import namedtuple
from random import randint

import cv2

from image_processing import get_centers_of_roi


# blue HSV threshold
MIN_T = (110, 128, 64)
MAX_T = (130, 256, 192)

CROSSHAIR_RADIUS = 30
CROSSHAIR_COLOR = (0, 186, 255)  # yellow

ENEMY_WIDTH = 100
ENEMY_HEIGHT = 120
ENEMY_COLOR = (0, 0, 255)  # red
ENEMY_SPAWN_RATE = 15
ENEMY_MAX_AGE = 30

HEALTH = 5
AMMO = 10
AMMO_SPAWN_RATE = 20

EDGE_OFFSET = 50

KILL_RADIUS = 50

ENEMIES = []

WIDTH = 1280
HEIGHT = 720

Enemy = namedtuple('Enemy', ['x', 'y', 'time_of_birth'])


def spawn_enemy(time):
    x = randint(EDGE_OFFSET, WIDTH - EDGE_OFFSET - ENEMY_WIDTH - 1)
    y = randint(EDGE_OFFSET, HEIGHT - EDGE_OFFSET - ENEMY_HEIGHT - 1)
    e = Enemy(x, y, time)
    ENEMIES.append(e)


def within(enemy, x, y):
    return (enemy.x < x < enemy.x + ENEMY_WIDTH
        and enemy.y < y < enemy.y + ENEMY_HEIGHT)


def draw_ammo(game_board, num_ammo):
    step = 20
    for i in range(num_ammo):
        cv2.rectangle(
            game_board,
            (step * (i + 1), step),
            (step * (i + 1) + 10, 3 * step),
            (255, 0, 0),
            -1
        )


def draw_crosshair(frame, game_board):
    centers = get_centers_of_roi(frame, MIN_T, MAX_T)
    if centers:
        area, x, y = centers[0]
        cv2.circle(game_board, (x, y), CROSSHAIR_RADIUS, CROSSHAIR_COLOR, 3)
        cv2.circle(game_board, (x, y), 5, CROSSHAIR_COLOR, 3)
        return x, y
    else:
        return None


def draw_enemies(game_board, image):
    magic = image[:,:,3]/255.0
    for enemy in ENEMIES:
        x, y = enemy.x, enemy.y

        for c in range(3):
            current_value = game_board[y:y+ENEMY_HEIGHT, x:x+ENEMY_WIDTH, c]
            game_board[y:y+ENEMY_HEIGHT, x:x+ENEMY_WIDTH, c] = (
                image[:,:,c] * magic + current_value * (1 - magic)
            )


def enemy_actions(game_board, time):
    acting_enemy = None
    for enemy in ENEMIES:
        if time - enemy.time_of_birth > ENEMY_MAX_AGE:
            acting_enemy = enemy
            break

    if acting_enemy is None:
        return False

    # TODO: do something
    cv2.circle(
        game_board, (acting_enemy.x, acting_enemy.y), 20, (0, 0, 255), -1)

    ENEMIES.remove(acting_enemy)
    return True


def main():
    game_over = False
    cv2.namedWindow('game')
    video = cv2.VideoCapture()
    video.open(0)
    counter, score, x, y = (0,) * 4
    health = HEALTH
    ammo = AMMO

    background = cv2.imread('background.png', -1)
    enemy_image = cv2.imread('enemy.png', -1)
    while True:

        if health == 0:
            game_over = True
            break

        counter += 1
        if counter % ENEMY_SPAWN_RATE == 0:
            spawn_enemy(counter)

        if counter % AMMO_SPAWN_RATE == 0:
            ammo += 1

        succ, frame = video.read()
        if not succ:
            video.release()
            break
        frame = cv2.flip(frame, 1)

        game_board = background.copy()
        #game_board = frame.copy()

        draw_ammo(game_board, ammo)
        draw_enemies(game_board, enemy_image)
        new_center = draw_crosshair(frame, game_board)
        if new_center is not None:
            x, y = new_center

        cv2.imshow('game', game_board)

        key = cv2.waitKey(100)
        if ammo and key == 32:  # space key
            ammo -= 1
            cv2.circle(background, (x, y), 3, (255, 0, 0), -1)
            enemies = ENEMIES  # needed to not mess up the looping
            for enemy in enemies:
                if within(enemy, x, y):
                    score += 1
                    ENEMIES.remove(enemy)
                    print('BOOM! Score: {0}'.format(score))

        hit = enemy_actions(background, counter)
        if hit:
            health -= 1

    if game_over:
        print('\nFINAL SCORE: {0}'.format(score))
        im = cv2.imread('gameover.png', -1)
        height, width, _ = im.shape
        background[50:50+height, 330:330+width] = im
        cv2.imshow('game', background)
        cv2.waitKey(0)

    video.release()


if __name__ == '__main__':
    main()
