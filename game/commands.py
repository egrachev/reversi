# -*- coding: utf-8 -*-

from kivy.uix.label import Label
from kivy.uix.popup import Popup

from .config import *
from .log import logger

HISTORY = list()


class Command(object):
    def execute(self):
        raise NotImplementedError()

    def cancel(self):
        raise NotImplementedError()


class UndoCommand(Command):
    def execute(self):
        try:
            command = HISTORY.pop()
            command.cancel()
        except IndexError:
            logger.log('HISTORY is empty')

    def cancel(self):
        pass


class MakeMoveCommand(Command):
    def __init__(self, cell, game):
        super(MakeMoveCommand, self).__init__()
        self.cell = cell
        self.game = game
        self.previous_states = []

    def execute(self):
        self.game.board.coords_state(self.cell.coord_x, self.cell.coord_y, PLAYERS_CELLS[self.game.current_player])

        win_cells = self.game.get_win_cells(self.cell)
        self.previous_states = [(i.coord_x, i.coord_y, i.state)for i in win_cells]

        for win_cell in win_cells:
            self.game.board.coords_state(win_cell.coord_x, win_cell.coord_y, self.cell.state)

        self.game.toggle_player()
        next_cells = self.game.get_next_cells()
        self.game.scores.calculate_score()

        if not next_cells:
            text = u'Победил - %s\n%s\n%s' % (
                PLAYERS_CELLS[self.game.current_player],
                self.game.scores.labels[PLAYER_WHITE].text,
                self.game.scores.labels[PLAYER_BLACK].text,
            )
            popup = Popup(title=u'Победитель', content=Label(text=text), size=(400, 400))
            popup.open()

            logger.log('Game over')

        HISTORY.append(self)

    def cancel(self):
        self.game.board.coords_state(self.cell.coord_x, self.cell.coord_y, CELL_STATE_EMPTY)

        for coord_x, coord_y, state in self.previous_states:
            self.game.board.coords_state(coord_x, coord_y, state)

        self.game.toggle_player()
        self.game.get_next_cells()
        self.game.scores.calculate_score()
