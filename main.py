import abc
import copy
import math

import pygame as pg
import sys
import os

from pygame.locals import *

FPS = 30
pg.init()
fpsClock = pg.time.Clock()

SCREEN_WIDTH, SCREEN_HEIGHT = 720, 640
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pg.time.Clock()

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


class Staff(object):
    STAFF_POS = [15, 15]
    STAFF_WIDTH = 680
    STAFF_HEIGHT = 600
    COLOR = (0, 0, 0)

    HEADROOM_TOP = 150
    HEADROOM_BOTTOM = 100
    INTER_STAFF_HEAD_ROOM = 150

    HEADROOM_LEFT = 20
    HEADROOM_RIGHT = 20
    STAFF_LINE_WEIGHT = LINE_WEIGHT_STANDARD

    NOTE_SPACE_WIDTH = 18
    NOTE_Y_RADIUS = math.floor((NOTE_SPACE_WIDTH + STAFF_LINE_WEIGHT) / 2)
    NOTE_OBLONGNESS = 3  # lol
    NOTE_X_RADIUS = NOTE_Y_RADIUS + NOTE_OBLONGNESS

    INDIVIDUAL_CLEF_HEIGHT = 5 * STAFF_LINE_WEIGHT + 4 * NOTE_SPACE_WIDTH
    INDIVIDUAL_CLEF_WIDTH = STAFF_WIDTH - (HEADROOM_LEFT + HEADROOM_RIGHT)

    TREBLE_CLEF_POS = [STAFF_POS[0] + HEADROOM_LEFT, STAFF_POS[1] + HEADROOM_TOP]
    BASS_CLEF_POS = \
        [STAFF_POS[0] + HEADROOM_LEFT, STAFF_POS[1] + HEADROOM_TOP + INDIVIDUAL_CLEF_HEIGHT + INTER_STAFF_HEAD_ROOM]

    TREBLE_IMAGE_SCALE = 0.75
    TREBLE_IMAGE_HEADROOM_LEFT = 0
    TREBLE_IMAGE_ANCHOR_OFFSET = 0.625

    BASS_IMAGE_SCALE = 0.32
    BASS_IMAGE_HEADROOM_LEFT = 35
    BASS_IMAGE_ANCHOR_OFFSET = 0.27

    CLEF_PLAY_AREA_OFFSET = 150 # TODO function of key signature
    CLEF_PLAY_AREA_POS = [STAFF_POS[0] + CLEF_PLAY_AREA_OFFSET, STAFF_POS[1]]

    def __init__(self):
        self.STAFF_TOP_RIGHT_CORNER = copy.deepcopy(self.STAFF_POS)
        self.STAFF_TOP_RIGHT_CORNER[0] = self.STAFF_TOP_RIGHT_CORNER[0] + self.STAFF_WIDTH
        self.STAFF_BOTTOM_LEFT_CORNER = copy.deepcopy(self.STAFF_POS)
        self.STAFF_BOTTOM_LEFT_CORNER[1] = self.STAFF_BOTTOM_LEFT_CORNER[1] + self.STAFF_HEIGHT

        self.treble_line_heights = self.get_clef_line_heights(self.TREBLE_CLEF_POS)
        self.treble_space_heights = self.get_clef_space_heights(self.treble_line_heights)
        self.bass_line_heights = self.get_clef_line_heights(self.BASS_CLEF_POS)
        self.bass_space_heights = self.get_clef_space_heights(self.bass_line_heights)

        self.display_heights = self.get_display_heights()

    def get_clef_space_heights(self, line_heights):
        res = []
        for i in range(0, len(line_heights) - 1):
            res.append(math.ceil((line_heights[i] + line_heights[i + 1]) / 2))
        return res

    # image offset_anchor is what percent of the way down the image is the anchor note height
    # e.g., the treble clef wants the curly bit to be in G4 and the bass clef wants F3 between the dots theah
    def draw_clef_symbol(self, image_file, image_scale, image_offset_anchor, image_headroom_left, note_height, surf):
        treble_image = pg.transform.rotozoom(pg.image.load(get_asset_file(image_file)).convert_alpha(), 0,
                                             image_scale)
        clef_symbol_y = note_height - math.floor(treble_image.get_height() * image_offset_anchor)
        surf.blit(treble_image, [self.STAFF_POS[0] + image_headroom_left, clef_symbol_y])

    def get_clef_line_heights(self, clef_pos):
        res = []
        for i in range(0, 5):
            line_height = clef_pos[1] + i * (self.NOTE_SPACE_WIDTH + self.STAFF_LINE_WEIGHT)
            res.append(line_height)
        return res

    def draw_clef_lines(self, clef_pos, line_heights, surf):
        draw_line_vertical(surf, self.COLOR, clef_pos, self.INDIVIDUAL_CLEF_HEIGHT, LINE_WEIGHT_BOLD)
        draw_line_vertical(surf, self.COLOR, [clef_pos[0] + self.INDIVIDUAL_CLEF_WIDTH, clef_pos[1]],
                           self.INDIVIDUAL_CLEF_HEIGHT, LINE_WEIGHT_BOLD)
        draw_line_vertical(surf, self.COLOR, [clef_pos[0] + self.CLEF_PLAY_AREA_OFFSET, clef_pos[1]],
                           self.INDIVIDUAL_CLEF_HEIGHT, LINE_WEIGHT_STANDARD)

        for line_height in line_heights:
            line_pos = [clef_pos[0], line_height]
            draw_line_horizontal(surf, self.COLOR, line_pos, self.INDIVIDUAL_CLEF_WIDTH, self.STAFF_LINE_WEIGHT)
        return line_heights

    def draw(self, surf):
        # outer bounding rectangle
        outer_bound_lw = LINE_WEIGHT_LIGHT
        draw_line_vertical(surf, self.COLOR, self.STAFF_POS, self.STAFF_HEIGHT, outer_bound_lw)
        draw_line_vertical(surf, self.COLOR, self.STAFF_TOP_RIGHT_CORNER, self.STAFF_HEIGHT, outer_bound_lw)
        draw_line_horizontal(surf, self.COLOR, self.STAFF_POS, self.STAFF_WIDTH, outer_bound_lw)
        draw_line_horizontal(surf, self.COLOR, self.STAFF_BOTTOM_LEFT_CORNER, self.STAFF_WIDTH + outer_bound_lw,
                             outer_bound_lw)

        # clef lines
        self.draw_clef_lines(self.TREBLE_CLEF_POS, self.treble_line_heights, surf)
        self.draw_clef_lines(self.BASS_CLEF_POS, self.bass_line_heights, surf)

        self.draw_clef_symbol("treble_clef.png", self.TREBLE_IMAGE_SCALE, self.TREBLE_IMAGE_ANCHOR_OFFSET,
                              self.TREBLE_IMAGE_HEADROOM_LEFT, self.treble_line_heights[3], surf)
        self.draw_clef_symbol("bass_clef.png", self.BASS_IMAGE_SCALE, self.BASS_IMAGE_ANCHOR_OFFSET,
                              self.BASS_IMAGE_HEADROOM_LEFT, self.bass_line_heights[1], surf)


    def get_note_rect(self, x_pos, note_height_id, scale = 1):
        left = x_pos - self.NOTE_X_RADIUS * scale
        top = note_height_id - self.NOTE_Y_RADIUS * scale
        width = self.NOTE_X_RADIUS * 2 * scale
        height = self.NOTE_Y_RADIUS * 2 * scale
        return pg.Rect(left, top, width, height)

    def get_display_heights(self):
        width = (self.NOTE_SPACE_WIDTH + self.STAFF_LINE_WEIGHT) / 2
        heights = {
            "D6_TREBLE": self.treble_line_heights[0] - 5 * width,
            "C6_TREBLE": self.treble_line_heights[0] - 4 * width,
            "B6_TREBLE": self.treble_line_heights[0] - 3 * width,
            "A6_TREBLE": self.treble_line_heights[0] - 2 * width,
            "G5_TREBLE": self.treble_line_heights[0] - 1 * width,

            "F5_TREBLE": self.treble_line_heights[0],
            "E5_TREBLE": self.treble_space_heights[0],
            "B5_TREBLE": self.treble_line_heights[1],
            "C5_TREBLE": self.treble_space_heights[1],
            "D5_TREBLE": self.treble_line_heights[2],
            "A5_TREBLE": self.treble_space_heights[2],
            "G4_TREBLE": self.treble_line_heights[3],
            "F4_TREBLE": self.treble_space_heights[3],
            "E4_TREBLE": self.treble_line_heights[4],

            "D4_TREBLE": self.treble_line_heights[4] + 1 * width,
            "C4_TREBLE": self.treble_line_heights[4] + 2 * width,
            "B4_TREBLE": self.treble_line_heights[4] + 3 * width,
            "A4_TREBLE": self.treble_line_heights[4] + 4 * width,
            "G3_TREBLE": self.treble_line_heights[4] + 5 * width,

            "F4_BASS": self.bass_line_heights[0] - 5 * width,
            "E4_BASS": self.bass_line_heights[0] - 4 * width,
            "D4_BASS": self.bass_line_heights[0] - 3 * width,
            "C4_BASS": self.bass_line_heights[0] - 2 * width,
            "B4_BASS": self.bass_line_heights[0] - 1 * width,

            "A4_BASS": self.bass_line_heights[0],
            "G3_BASS": self.bass_space_heights[0],
            "F3_BASS": self.bass_line_heights[1],
            "E3_BASS": self.bass_space_heights[1],
            "D3_BASS": self.bass_line_heights[2],
            "C3_BASS": self.bass_space_heights[2],
            "B3_BASS": self.bass_line_heights[3],
            "A3_BASS": self.bass_space_heights[3],
            "G2_BASS": self.bass_line_heights[4],

            "F2_BASS": self.bass_line_heights[4] + 1 * width,
            "E2_BASS": self.bass_line_heights[4] + 2 * width,
            "D2_BASS": self.bass_line_heights[4] + 3 * width,
            "C2_BASS": self.bass_line_heights[4] + 4 * width,
            "B2_BASS": self.bass_line_heights[4] + 5 * width,

        }
        return heights

from enum import Enum
class NoteCollisionSideEffect(Enum):
    NONE = 0
    PLAYER_MISSED_ALL = 1
    ENEMY_NOTE_GOT_THROUGH = 2
    SUCCESSFUL_COLLISION_PLAYER = 3
    SUCCESSFUL_COLLISION_ENEMY = 4

class GameState():

    SCORE_FONT_SIZE = 24
    SCORE_POSITION = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 16]

    def __init__(self, staff):
        self.staff = staff
        self.player_notes = dict()
        self.enemy_notes = dict()
        self.latest_note_id = 0
        self.score = 0

        self.SCORE_POSITION = [staff.STAFF_POS[0] + staff.STAFF_WIDTH / 2, staff.STAFF_HEIGHT / 12]

    def update(self):
        for (id, note) in self.player_notes.items():
            note.update()
        for (id, note) in self.enemy_notes.items():
            note.update()

        # TODO efficientize
        for (player_note_id, player_note) in self.player_notes.items():
            for (enemy_note_id, enemy_note) in self.enemy_notes.items():
                enemy_note.try_interact(player_note)

        player_notes_to_destroy = []
        enemy_notes_to_destroy = []
        side_effects = []

        for (id, note) in self.player_notes.items():
            side_effect =  note.should_destroy
            if side_effect:
                player_notes_to_destroy.append(id)
                side_effects.append(side_effect)

        for (id, note) in self.enemy_notes.items():
            side_effect = note.should_destroy
            if side_effect:
                enemy_notes_to_destroy.append(id)
                side_effects.append(side_effect)

        for id in player_notes_to_destroy:
            del self.player_notes[id]

        for id in enemy_notes_to_destroy:
            del self.enemy_notes[id]

        for side_effect in side_effects:
            self.do_side_effect(side_effect)

    def do_side_effect(self, side_effect: NoteCollisionSideEffect):
        print(side_effect)
        if side_effect == NoteCollisionSideEffect.NONE:
            return
        elif side_effect == NoteCollisionSideEffect.SUCCESSFUL_COLLISION_ENEMY:
            self.score += 1
        elif side_effect == NoteCollisionSideEffect.ENEMY_NOTE_GOT_THROUGH:
            self.score -= 1
        elif side_effect == NoteCollisionSideEffect.PLAYER_MISSED_ALL:
            self.score -= 1
        return

    def draw_note_collection(self, surf, staff):
        for (id, note) in self.enemy_notes.items():
            note.draw(surf, staff)

        for (id, note) in self.player_notes.items():
            note.draw(surf, staff)

    antialias_score = True
    score_color = (255, 0, 0)

    def draw_score(self, surf):
        my_ft_font = pg.font.SysFont('Times New Roman', self.SCORE_FONT_SIZE)
        text_surface = my_ft_font.render(f"Score: {self.score}", self.antialias_score, self.score_color)
        surf.blit(text_surface, self.SCORE_POSITION)

    def draw(self, surf):
        self.draw_note_collection(surf, self.staff)
        self.draw_score(surf)

    def register_player_note(self, note):
        self.player_notes[self.latest_note_id] = note
        self.latest_note_id += 1

    def register_enemy_note(self, note):
        self.enemy_notes[self.latest_note_id] = note
        self.latest_note_id += 1


class Note:
    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def should_destroy(self):
        pass


    @abc.abstractmethod
    def note_real_value(self):
        pass

    @abc.abstractmethod
    def draw(self, surf, staff):
        pass



class PlayerShot(Note):
    PLAYER_SHOT_SPEED = 5

    @property
    def note_real_value(self):
        return self.midi_num

    def __init__(self, midi_num, midi_vel, x_init, x_thresh):
        self.x_thresh = x_thresh # todo
        self.midi_num = midi_num
        self.midi_vel = midi_vel
        self.x_position = x_init
        self.should_be_destroyed = False
        self.side_effect = None

    def update(self):
        self.x_position = self.x_position + self.PLAYER_SHOT_SPEED
        if self.x_position > self.x_thresh:
            self.should_be_destroyed = True
            self.side_effect = NoteCollisionSideEffect.PLAYER_MISSED_ALL

    @property
    def should_destroy(self):
        return self.side_effect

    def draw(self, surf, staff):
        note_height_id = self.midi_num #TODO: NONSENSE
        note_height = staff.display_heights[note_height_id]
        draw_ellipse_angle(surf, (0,125,0,255), staff.get_note_rect(self.x_position, note_height), 20) # TODO: DRY/Refactor





class BasicEnemyNote(Note):
    def __init__(self, x_init, midi_num, x_thresh, collision_thresh):
        self.x_thresh = x_thresh
        self.ENEMY_NOTE_SPEED = -3
        self.midi_num = midi_num
        self.x_position = x_init
        self.side_effect = None
        self.collision_thresh = collision_thresh

    @property
    def note_real_value(self):
        return self.midi_num

    @property
    def should_destroy(self):
        return self.side_effect

    def draw(self, surf, staff):
        note_height_id = self.midi_num # TODO: Nonsense
        note_height = staff.display_heights[note_height_id]
        draw_ellipse_angle(surf, (255,0,0,255), staff.get_note_rect(self.x_position, note_height), 20) # TODO: DRY/Refactor

    def update(self):
        self.x_position += self.ENEMY_NOTE_SPEED
        if self.x_position < self.x_thresh:
            self.side_effect = NoteCollisionSideEffect.ENEMY_NOTE_GOT_THROUGH


    def try_interact(self, player_note):
        if not self.side_effect:
            if self.collides_with_player_note(player_note):
                self.side_effect = NoteCollisionSideEffect.SUCCESSFUL_COLLISION_ENEMY
                player_note.side_effect = NoteCollisionSideEffect.SUCCESSFUL_COLLISION_PLAYER

    def collides_with_player_note(self, player_note):
        return self.midi_num == player_note.midi_num and \
               abs(self.x_position - player_note.x_position) < self.collision_thresh



def new_surface():
    surface = pg.Surface(screen.get_size(), pg.SRCALPHA)
    surface = surface.convert_alpha()
    return surface


def draw_ellipse_angle(surf, color, rect, angle):
    shape_surf = pg.Surface(rect.size, pg.SRCALPHA)
    pg.draw.ellipse(shape_surf, color, (0, 0, rect.width, rect.height))
    rotated_surf = pg.transform.rotate(shape_surf, angle)
    surf.blit(rotated_surf, rotated_surf.get_rect(center=rect.center))


if __name__ == '__main__':

    # Pre-render staff surface
    staff_surface = new_surface()
    staff_surface.fill((255, 255, 255, 255))
    staff = Staff()
    staff.draw(staff_surface)

    gamestate = GameState(staff)
    note_surface = new_surface()

    while True:

        for event in pg.event.get():
            print(event)
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    gamestate.register_player_note(
                        PlayerShot("G4_TREBLE", 999, staff.CLEF_PLAY_AREA_POS[0], staff.STAFF_TOP_RIGHT_CORNER[0])
                    )
                if event.key == K_RIGHT:
                    gamestate.register_player_note(
                        PlayerShot("A5_TREBLE", 999, staff.CLEF_PLAY_AREA_POS[0], staff.STAFF_TOP_RIGHT_CORNER[0])
                    )
                elif event.key == K_DOWN:
                    gamestate.register_enemy_note(
                        BasicEnemyNote(staff.STAFF_TOP_RIGHT_CORNER[0], "G4_TREBLE", staff.CLEF_PLAY_AREA_POS[0], staff.NOTE_X_RADIUS)
                    )
                elif event.key == K_LEFT:
                    gamestate.register_enemy_note(
                        BasicEnemyNote(staff.STAFF_TOP_RIGHT_CORNER[0], "A5_TREBLE", staff.CLEF_PLAY_AREA_POS[0], staff.NOTE_X_RADIUS)
                    )

        gamestate.update()
        # font = pg.font.Font(None, 36)
        # text = font.render(str(snake.length), 1, (10, 10, 10))
        # textpos = text.get_rect()
        # textpos.centerx = 20
        # surface.blit(text, textpos)

        note_surface.fill((255,255,255,0))
        gamestate.draw(note_surface)

        screen.blit(staff_surface, (0, 0))
        screen.blit(note_surface, (0, 0))

        pg.display.flip()
        pg.display.update()
        fpsClock.tick(FPS)
