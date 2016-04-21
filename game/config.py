# -*- coding: utf-8 -*-

from kivy.uix.image import Image


WINDOW_WIDTH = 530
WINDOW_HEIGHT = 640

BOARD_SIZE = 8

CELL_STATE_WHITE = 'white'
CELL_STATE_BLACK = 'black'
CELL_STATE_EMPTY = 'empty'
CELL_STATE_STEP = 'step'

CELL_STATES = [
    CELL_STATE_WHITE,
    CELL_STATE_BLACK,
    CELL_STATE_EMPTY,
    CELL_STATE_STEP
]

CELLS_TEXTURES = {
    CELL_STATE_WHITE: Image(source='icons/white.png').texture,
    CELL_STATE_BLACK: Image(source='icons/black.png').texture,
    CELL_STATE_EMPTY: Image(source='icons/empty.png').texture,
    CELL_STATE_STEP: Image(source='icons/step.png').texture,
}

PLAYER_WHITE = '1'
PLAYER_BLACK = '2'
PLAYERS_CELLS = {
    PLAYER_WHITE: CELL_STATE_WHITE,
    PLAYER_BLACK: CELL_STATE_BLACK,
}