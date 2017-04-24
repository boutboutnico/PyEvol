import pygame
import math

from color import *


def polar_to_cartesian(r, theta):
    '''r: vector magnitude
    theta: vector direction (radians)
    return: (x,y) cartesian coordinates'''

    return r * math.cos(theta), r * math.sin(theta)


def rotate(point, pivot, angle):
    '''px, py: pivot point
    angle : radians'''

    c = math.cos(angle)
    s = math.sin(angle)

    (px, py) = pivot
    (x, y) = point

    x -= px
    y -= py

    x_new = x * c - y * s
    y_new = x * s + y * c

    return int(x_new + px), int(y_new + py)


class Creature:

    SIZE = 50
    half_size = int(SIZE / 2)
    quarter_size = int(SIZE / 4)
    body_draw_pos = (int(SIZE / 2), int(SIZE / 2))
    body_radius = int(SIZE / 2)
    eye_radius = 5
    eye_left_pos = (int(SIZE * 3 / 4), int(SIZE / 2 - SIZE / 4))
    eye_right_pos = (int(SIZE * 3 / 4), int(SIZE / 2 + SIZE / 4))

    POWER_MIN = 0
    ENGINE_ANGLE = math.radians(45)

    def __init__(self):
        self.x = 400
        self.y = 400
        self.theta = math.radians(0) # radians
        self.color = GREEN
        # self.surface = pygame.surface.Surface((Creature.size, Creature.size))

        (self.left_power, self.right_power) = (0,0)

    def move(self, left_power, right_power):

        self.left_power = max(left_power, Creature.POWER_MIN)
        self.right_power = max(right_power, Creature.POWER_MIN)

        (x_l, y_l) = polar_to_cartesian(self.left_power, self.theta + Creature.ENGINE_ANGLE)
        (x_r, y_r) = polar_to_cartesian(self.right_power, self.theta - Creature.ENGINE_ANGLE)

        x_result = x_l + x_r
        y_result = y_l + y_r

        self.x += int(x_result)
        self.y += int(y_result)

        if self.left_power != 0 or self.right_power != 0:
            self.theta = math.atan2(y_result, x_result)

    def render(self, surface):
        # Body
        pygame.draw.circle(surface, self.color, (self.x, self.y), Creature.body_radius)

        # Eyes
        eye_pos = (self.x + Creature.quarter_size, self.y - Creature.quarter_size)
        eye_pos = rotate(eye_pos, (self.x,self.y), self.theta)
        pygame.draw.circle(surface, BLACK, eye_pos, Creature.eye_radius)

        eye_pos = (self.x + Creature.quarter_size, self.y + Creature.quarter_size)
        eye_pos = rotate(eye_pos, (self.x, self.y), self.theta)
        pygame.draw.circle(surface, BLACK, eye_pos, Creature.eye_radius)

        ##########

        # # # Body
        # pygame.draw.circle(self.surface, self.color, Creature.body_draw_pos, Creature.body_radius)
        #
        # # Eyes
        # pygame.draw.circle(self.surface, BLACK, Creature.eye_left_pos, Creature.eye_radius)
        # pygame.draw.circle(self.surface, BLACK, Creature.eye_right_pos, Creature.eye_radius)
        #
        # surface.blit(pygame.transform.rotate(self.surface, self.theta), (self.x - Creature.half_size, self.y - Creature.half_size))

