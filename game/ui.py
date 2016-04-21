# -*- coding: utf-8 -*-

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import OptionProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

from .config import *
from .commands import MakeMoveCommand, UndoCommand
from .log import logger


class BoardCell(Image):
    state = OptionProperty(CELL_STATE_EMPTY, options=CELL_STATES)

    def __init__(self, **kwargs):
        self.coord_x = kwargs.get('coord_x', 0)
        self.coord_y = kwargs.get('coord_y', 0)

        super(BoardCell, self).__init__(**kwargs)

        self.width = 128
        self.height = 128

        self.texture = CELLS_TEXTURES[CELL_STATE_EMPTY]

    def __unicode__(self):
        return 'cell[%s,%s|%s]' % (self.coord_x, self.coord_y, self.state)

    def __str__(self):
        return 'cell[%s,%s|%s]' % (self.coord_x, self.coord_y, self.state)

    def on_state(self, instance, value):
        self.texture = CELLS_TEXTURES[value]

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.state == CELL_STATE_STEP:
                from . import ReversiGame

                game = ReversiGame()
                command = MakeMoveCommand(self, game)
                command.execute()


class Board(GridLayout):
    def coords(self, x, y):
        try:
            cell = self.coords_cells[x-1][y-1]
            return cell
        except IndexError:
            logger.log('[%s, %s] - missing' % (x, y))

    def coords_state(self, x, y, state):
        cell = self.coords(x, y)

        cell.state = state

        for i in CELL_STATES:
            if cell in self.cells[i]:
                self.cells[i].remove(cell)

            if i == state:
                self.cells[state].append(cell)

    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)

        self.coords_cells = []
        self.cells = {
            CELL_STATE_WHITE: [],
            CELL_STATE_BLACK: [],
            CELL_STATE_STEP: [],
            CELL_STATE_EMPTY: [],
        }

        self.cols = BOARD_SIZE
        self.rows = BOARD_SIZE

        self.col_force_default = True
        self.row_force_default = True

        self.col_default_width = 64
        self.row_default_height = 64


class Scores(BoxLayout):
    def __init__(self, **kwargs):
        super(Scores, self).__init__(**kwargs)

        self.orientation = 'horizontal'
        self.size_hint_y = 0.2

        self.labels = {}
        self.labels[PLAYER_WHITE] = Label(text='', size_hint_x=.4, markup=True, bold=True)
        self.labels[PLAYER_BLACK] = Label(text='', size_hint_x=.4, markup=True)

        self.btn_undo = Button(text='Undo', size_hint_x=.2)
        self.btn_undo.bind(on_press=self.undo_handler)

        self.add_widget(self.labels[PLAYER_WHITE])
        self.add_widget(self.btn_undo)
        self.add_widget(self.labels[PLAYER_BLACK])

    def calculate_score(self):
        from . import ReversiGame

        game = ReversiGame()
        self.labels[PLAYER_WHITE].text = 'White: %s' % len(game.board.cells[CELL_STATE_WHITE])
        self.labels[PLAYER_BLACK].text = 'Black: %s' % len(game.board.cells[CELL_STATE_BLACK])

    def undo_handler(self, instance):
        command = UndoCommand()
        command.execute()

        logger.log('Undo command')

class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
