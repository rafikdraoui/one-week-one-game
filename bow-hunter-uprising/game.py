#!/usr/bin/env python

from collections import namedtuple
from math import sqrt
from random import randint

import cv2

from image_processing import get_centers_of_roi


# blue HSV threshold
MIN_T = (110, 128, 64)
MAX_T = (130, 256, 192)

CROSSHAIR_RADIUS = 30
CROSSHAIR_COLOR = (0, 186, 255)  # yellow

ENEMY_RADIUS = 50
ENEMY_COLOR = (0, 0, 255)  # red
ENEMY_SPAWN_RATE = 30

ENEMIES = []

WIDTH = 1280
HEIGHT = 720

Enemy = namedtuple('Enemy', ['x', 'y', 'size'])


square = lambda x: x * x


def spawn_enemy():
    x = randint(ENEMY_RADIUS, WIDTH - ENEMY_RADIUS - 1)
    y = randint(ENEMY_RADIUS, HEIGHT - ENEMY_RADIUS - 1)
    e = Enemy(x, y, ENEMY_RADIUS)
    ENEMIES.append(e)


def within(enemy, x, y):
    dist = sqrt(square(enemy.x - x) + square(enemy.y - y))
    #return dist < ENEMY_RADIUS
    return dist < 1.5 * ENEMY_RADIUS


def draw_crosshair(frame):
    centers = get_centers_of_roi(frame, MIN_T, MAX_T)
    if centers:
        area, x, y = centers[0]
        cv2.circle(frame, (x, y), CROSSHAIR_RADIUS, CROSSHAIR_COLOR, 3)
        cv2.circle(frame, (x, y), 5, CROSSHAIR_COLOR, 3)
        return x, y
    else:
        return None


def draw_enemies(frame):
    for enemy in ENEMIES:
        center = enemy.x, enemy.y
        cv2.circle(frame, center, enemy.size, ENEMY_COLOR, -1)


def main():
    cv2.namedWindow('game')
    video = cv2.VideoCapture()
    video.open(0)
    counter, score, x, y = (0,) * 4

    while True:
        counter += 1
        if counter % ENEMY_SPAWN_RATE == 0:
            spawn_enemy()

        succ, frame = video.read()
        if not succ:
            video.release()
            break

        frame = cv2.flip(frame, 1)
        draw_enemies(frame)
        new_center = draw_crosshair(frame)
        if new_center is not None:
            x, y = new_center

        cv2.imshow('game', frame)

        enemies = ENEMIES  # needed to not mess up the looping
        for enemy in enemies:
            if within(enemy, x, y):
                score += 1
                ENEMIES.remove(enemy)
                print('BOOM! Score: {0}'.format(score))

        key = cv2.waitKey(100)
        if key == 32:  # space key
            print('\nFINAL SCORE: {0}'.format(score))
            break

    video.release()


if __name__ == '__main__':
    main()
