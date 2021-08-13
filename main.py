import copy

import pygame
import sys
import random

from pygame.locals import *

FPS = 30
pygame.init()
fpsClock = pygame.time.Clock()

SCREEN_WIDTH, SCREEN_HEIGHT = 720, 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pygame.time.Clock()

pygame.key.set_repeat(1, 40)

GRIDSIZE = 10
GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE
LINE_WEIGHT_BOLD = 8
LINE_WEIGHT_STANDARD = 2
LINE_WEIGHT_LIGHT = 1

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def draw_line_horizontal(surf, color, pos, width, line_weight=LINE_WEIGHT_STANDARD):
    r = pygame.Rect((pos[0], pos[1]), (width, line_weight))
    pygame.draw.rect(surf, color, r)


def draw_line_vertical(surf, color, pos, height, line_weight=LINE_WEIGHT_STANDARD):
    r = pygame.Rect((pos[0], pos[1]), (line_weight, height))
    pygame.draw.rect(surf, color, r)


def draw_circle(surf, color, pos):
    r = pygame.Rect((pos[0], pos[1]), (GRIDSIZE, GRIDSIZE))
    pygame.draw.ellipse(surf, color, r)


class Staff(object):
    STAFF_POS = [15, 15]
    STAFF_WIDTH = 600
    STAFF_HEIGHT = 450
    COLOR = (0, 0, 0)

    HEADROOM_TOP = 80
    HEADROOM_BOTTOM = 100
    INTER_STAFF_HEAD_ROOM = 150

    HEADROOM_LEFT = 20
    HEADROOM_RIGHT = 20
    STAFF_LINE_WEIGHT = LINE_WEIGHT_STANDARD

    TREBLE_CLEF_POS = [STAFF_POS[0] + HEADROOM_LEFT, STAFF_POS[1] + HEADROOM_TOP]
    TREBLE_CLEF_END = [STAFF_POS[0] + STAFF_WIDTH - HEADROOM_RIGHT, STAFF_POS[1] + HEADROOM_TOP]

    NOTE_SPACE_WIDTH = 15

    INDIVIDUAL_CLEF_HEIGHT = 5 * STAFF_LINE_WEIGHT + 4 * NOTE_SPACE_WIDTH
    INDIVIDUAL_CLEF_WIDTH = STAFF_WIDTH - (HEADROOM_LEFT + HEADROOM_RIGHT)

    def __init__(self):
        self.STAFF_TOP_RIGHT_CORNER = copy.deepcopy(self.STAFF_POS)
        self.STAFF_TOP_RIGHT_CORNER[0] = self.STAFF_TOP_RIGHT_CORNER[0] + self.STAFF_WIDTH
        self.STAFF_BOTTOM_LEFT_CORNER = copy.deepcopy(self.STAFF_POS)
        self.STAFF_BOTTOM_LEFT_CORNER[1] = self.STAFF_BOTTOM_LEFT_CORNER[1] + self.STAFF_HEIGHT

    def draw(self, surf):
        # outer bounding rectangle
        outer_bound_lw = LINE_WEIGHT_LIGHT
        draw_line_vertical(surf, self.COLOR, self.STAFF_POS, self.STAFF_HEIGHT, outer_bound_lw)
        draw_line_vertical(surf, self.COLOR, self.STAFF_TOP_RIGHT_CORNER, self.STAFF_HEIGHT, outer_bound_lw)
        draw_line_horizontal(surf, self.COLOR, self.STAFF_POS, self.STAFF_WIDTH, outer_bound_lw)
        draw_line_horizontal(surf, self.COLOR, self.STAFF_BOTTOM_LEFT_CORNER, self.STAFF_WIDTH + outer_bound_lw,
                             outer_bound_lw)

        # treble clef
        draw_line_vertical(surf, self.COLOR, self.TREBLE_CLEF_POS, self.INDIVIDUAL_CLEF_HEIGHT, LINE_WEIGHT_BOLD)
        draw_line_vertical(surf, self.COLOR, self.TREBLE_CLEF_END, self.INDIVIDUAL_CLEF_HEIGHT, LINE_WEIGHT_BOLD)

        for i in range(0,5):
            line_pos = \
                [self.TREBLE_CLEF_POS[0], self.TREBLE_CLEF_POS[1] + i* (self.NOTE_SPACE_WIDTH + self.STAFF_LINE_WEIGHT)]
            draw_line_horizontal(surf, self.COLOR, line_pos, self.INDIVIDUAL_CLEF_WIDTH, self.STAFF_LINE_WEIGHT)





def new_surface():
    surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    surface = surface.convert_alpha()
    return surface


if __name__ == '__main__':

    # Pre-render staff surface
    staff_surface = new_surface()
    staff_surface.fill((255, 255, 255, 255))
    staff = Staff()
    staff.draw(staff_surface)

    while True:

        for event in pygame.event.get():
            print(event)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # elif event.type == KEYDOWN:
            #     if event.key == K_UP:
            #         snake.point(UP)
            #     elif event.key == K_DOWN:
            #         snake.point(DOWN)
            #     elif event.key == K_LEFT:
            #         snake.point(LEFT)
            #     elif event.key == K_RIGHT:
            #         snake.point(RIGHT)

        # font = pygame.font.Font(None, 36)
        # text = font.render(str(snake.length), 1, (10, 10, 10))
        # textpos = text.get_rect()
        # textpos.centerx = 20
        # surface.blit(text, textpos)

        screen.blit(staff_surface, (0, 0))

        pygame.display.flip()
        pygame.display.update()
        fpsClock.tick(FPS)
