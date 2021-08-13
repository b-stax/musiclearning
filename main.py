import copy
import math

import pygame as pg
import sys
import os

from pygame.locals import *

FPS = 30
pg.init()
fpsClock = pg.time.Clock()

SCREEN_WIDTH, SCREEN_HEIGHT = 840, 480
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pg.time.Clock()

pg.key.set_repeat(1, 40)

GRIDSIZE = 10
GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE
LINE_WEIGHT_BOLD = 8
LINE_WEIGHT_STANDARD = 2
LINE_WEIGHT_LIGHT = 1

main_dir = os.path.split(os.path.abspath(__file__))[0]


def get_asset_file(file):
    return os.path.join(main_dir, "assets", file)


def draw_line_horizontal(surf, color, pos, width, line_weight=LINE_WEIGHT_STANDARD):
    r = pg.Rect((pos[0], pos[1]), (width, line_weight))
    pg.draw.rect(surf, color, r)


def draw_line_vertical(surf, color, pos, height, line_weight=LINE_WEIGHT_STANDARD):
    r = pg.Rect((pos[0], pos[1]), (line_weight, height))
    pg.draw.rect(surf, color, r)


def draw_circle(surf, color, pos):
    r = pg.Rect((pos[0], pos[1]), (GRIDSIZE, GRIDSIZE))
    pg.draw.ellipse(surf, color, r)


class Staff(object):
    STAFF_POS = [15, 15]
    STAFF_WIDTH = 750
    STAFF_HEIGHT = 450
    COLOR = (0, 0, 0)

    HEADROOM_TOP = 80
    HEADROOM_BOTTOM = 100
    INTER_STAFF_HEAD_ROOM = 150

    HEADROOM_LEFT = 20
    HEADROOM_RIGHT = 20
    STAFF_LINE_WEIGHT = LINE_WEIGHT_STANDARD

    NOTE_SPACE_WIDTH = 15

    INDIVIDUAL_CLEF_HEIGHT = 5 * STAFF_LINE_WEIGHT + 4 * NOTE_SPACE_WIDTH
    INDIVIDUAL_CLEF_WIDTH = STAFF_WIDTH - (HEADROOM_LEFT + HEADROOM_RIGHT)

    TREBLE_CLEF_POS = [STAFF_POS[0] + HEADROOM_LEFT, STAFF_POS[1] + HEADROOM_TOP]
    BASS_CLEF_POS = \
        [STAFF_POS[0] + HEADROOM_LEFT, STAFF_POS[1] + HEADROOM_TOP + INDIVIDUAL_CLEF_HEIGHT + INTER_STAFF_HEAD_ROOM]

    def __init__(self):
        self.STAFF_TOP_RIGHT_CORNER = copy.deepcopy(self.STAFF_POS)
        self.STAFF_TOP_RIGHT_CORNER[0] = self.STAFF_TOP_RIGHT_CORNER[0] + self.STAFF_WIDTH
        self.STAFF_BOTTOM_LEFT_CORNER = copy.deepcopy(self.STAFF_POS)
        self.STAFF_BOTTOM_LEFT_CORNER[1] = self.STAFF_BOTTOM_LEFT_CORNER[1] + self.STAFF_HEIGHT

    def draw_clef_lines(self, clef_pos, surf):
        clef_top_right_corner = [clef_pos[0] + self.INDIVIDUAL_CLEF_WIDTH, clef_pos[1]]
        draw_line_vertical(surf, self.COLOR, clef_pos, self.INDIVIDUAL_CLEF_HEIGHT, LINE_WEIGHT_BOLD)
        draw_line_vertical(surf, self.COLOR, clef_top_right_corner, self.INDIVIDUAL_CLEF_HEIGHT, LINE_WEIGHT_BOLD)

        for i in range(0, 5):
            line_pos = \
                [clef_pos[0], clef_pos[1] + i * (self.NOTE_SPACE_WIDTH + self.STAFF_LINE_WEIGHT)]
            draw_line_horizontal(surf, self.COLOR, line_pos, self.INDIVIDUAL_CLEF_WIDTH, self.STAFF_LINE_WEIGHT)

    def draw(self, surf):
        # outer bounding rectangle
        outer_bound_lw = LINE_WEIGHT_LIGHT
        draw_line_vertical(surf, self.COLOR, self.STAFF_POS, self.STAFF_HEIGHT, outer_bound_lw)
        draw_line_vertical(surf, self.COLOR, self.STAFF_TOP_RIGHT_CORNER, self.STAFF_HEIGHT, outer_bound_lw)
        draw_line_horizontal(surf, self.COLOR, self.STAFF_POS, self.STAFF_WIDTH, outer_bound_lw)
        draw_line_horizontal(surf, self.COLOR, self.STAFF_BOTTOM_LEFT_CORNER, self.STAFF_WIDTH + outer_bound_lw,
                             outer_bound_lw)

        # clef lines
        self.draw_clef_lines(self.TREBLE_CLEF_POS, surf)
        self.draw_clef_lines(self.BASS_CLEF_POS, surf)

        # clef symbols
        treble_image_scale = 0.75
        treble_image = pg.transform.rotozoom(pg.image.load(get_asset_file("treble_clef.png")).convert_alpha(), 0,
                                             treble_image_scale)
        treble_image_anchor_offset = 0.625  # percent of the way down that needs to be on G4
        TREBLE_CLEF_HEADROOM = 0
        treble_y = 145 - math.floor(treble_image.get_height() * treble_image_anchor_offset)
        surf.blit(treble_image, [self.STAFF_POS[0] + TREBLE_CLEF_HEADROOM, treble_y])

        bass_image = pg.image.load(get_asset_file("bass_clef.png")).convert_alpha()
        bass_image_anchor_offset = 0.4  # position that needs to be on F3

        surf.blit(bass_image, (0, 0))


def new_surface():
    surface = pg.Surface(screen.get_size(), pg.SRCALPHA)
    surface = surface.convert_alpha()
    return surface


if __name__ == '__main__':

    # Pre-render staff surface
    staff_surface = new_surface()
    staff_surface.fill((255, 255, 255, 255))
    staff = Staff()
    staff.draw(staff_surface)

    while True:

        for event in pg.event.get():
            print(event)
            if event.type == QUIT:
                pg.quit()
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

        # font = pg.font.Font(None, 36)
        # text = font.render(str(snake.length), 1, (10, 10, 10))
        # textpos = text.get_rect()
        # textpos.centerx = 20
        # surface.blit(text, textpos)

        screen.blit(staff_surface, (0, 0))

        pg.display.flip()
        pg.display.update()
        fpsClock.tick(FPS)
