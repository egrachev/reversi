# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.properties import OptionProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window


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

Window.size = (530, 640)


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
            print('HISTORY is empty')

    def cancel(self):
        pass


class MakeMoveCommand(Command):
    def __init__(self, cell):
        super(MakeMoveCommand, self).__init__()
        self.cell = cell
        self.game = ReversiGame()
        self.previous_states = []

    def execute(self):
        self.game.board.coords_state(self.cell.coord_x, self.cell.coord_y, PLAYERS_CELLS[self.game.current_player])

        win_cells = self.game.get_win_cells(self.cell)
        self.previous_states = [(i.coord_x, i.coord_y, i.state)for i in win_cells]

        for win_cell in win_cells:
            self.game.board.coords_state(win_cell.coord_x, win_cell.coord_y, self.cell.state)

        self.game.toggle_player()
        self.game.get_next_cells()
        HISTORY.append(self)

    def cancel(self):
        self.game.board.coords_state(self.cell.coord_x, self.cell.coord_y, CELL_STATE_EMPTY)

        for coord_x, coord_y, state in self.previous_states:
            self.game.board.coords_state(coord_x, coord_y, state)

        self.game.toggle_player()



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
                command = MakeMoveCommand(self)
                command.execute()


class Board(GridLayout):
    def coords(self, x, y):
        try:
            cell = self.coords_cells[x-1][y-1]
            return cell
        except IndexError:
            print('[%s, %s] - missing' % (x, y))

    def coords_state(self, x, y, state):
        cell = self.coords(x, y)

        cell.state = state

        for i in CELL_STATES:
            if i == state:
                self.cells[state].append(cell)
            else:
                if cell in self.cells[i]:
                    self.cells[i].remove(cell)

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

class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'

class ReversiGame(object):
    instance = None

    def __new__(cls):
        if not cls.instance:
            cls.instance = super(ReversiGame, cls).__new__(cls)

        return cls.instance

    def compose(self, root):
        self.current_player = PLAYER_WHITE
        self.next_player = PLAYER_BLACK

        self.board = Board()
        self.board.padding = 10

        for x in range(BOARD_SIZE):
            self.board.coords_cells.append([])

            for y in range(BOARD_SIZE):
                broad_cell = BoardCell(coord_x=x+1, coord_y=y+1)
                self.board.coords_cells[x].append(broad_cell)
                self.board.add_widget(broad_cell)

        self.board.coords_state(BOARD_SIZE / 2, BOARD_SIZE / 2, state=CELL_STATE_WHITE)
        self.board.coords_state(BOARD_SIZE / 2 + 1, BOARD_SIZE / 2 + 1, state=CELL_STATE_WHITE)
        self.board.coords_state(BOARD_SIZE / 2, BOARD_SIZE / 2 + 1, state=CELL_STATE_BLACK)
        self.board.coords_state(BOARD_SIZE / 2 + 1, BOARD_SIZE / 2, state=CELL_STATE_BLACK)

        root.add_widget(self.board)

        self.scores = Scores()
        self.scores.size_hint_y = 0.2

        self.label_player1 = Label(text='Player 1', size_hint_x=.4)
        self.label_player2 = Label(text='Player 2', size_hint_x=.4)

        self.btn_undo = Button(text='Undo', size_hint_x=.2)
        self.btn_undo.bind(on_press=self.undo_handler)

        self.scores.add_widget(self.label_player1)
        self.scores.add_widget(self.btn_undo)
        self.scores.add_widget(self.label_player2)

        root.add_widget(self.scores)

        self.get_next_cells()

    def undo_handler(self, instance):
        command = UndoCommand()
        command.execute()

    def get_paths(self, cell):
        """
        game paths for cell
        """
        x = cell.coord_x
        y = cell.coord_y

        x_right = range(x+1, BOARD_SIZE+1)
        x_left = range(x-1, 0, -1)

        y_up = range(y-1, 0, -1)
        y_down = range(y+1, BOARD_SIZE+1)

        return [
            [(x, i) for i in y_up],
            [(x, i) for i in y_down],

            [(i, y) for i in x_left],
            [(i, y) for i in x_right],

            [(i, j) for i, j in zip(x_right, y_up)],
            [(i, j) for i, j in zip(x_right, y_down)],

            [(i, j) for i, j in zip(x_left, y_up)],
            [(i, j) for i, j in zip(x_left, y_down)],
        ]

    def reset_next_cells(self):
        cells = [(i.coord_x, i.coord_y)for i in self.board.cells[CELL_STATE_STEP]]
        for x, y in cells:
            self.board.coords_state(x, y, CELL_STATE_EMPTY)

    def get_win_cells(self, cell):
        self.reset_next_cells()
        cells = []

        for path in self.get_paths(cell):
            next_cell = self.check_path(path)

            if next_cell:
                for x, y in path:
                    cells.append(self.board.coords(x, y))

                    if next_cell.coord_x == x and next_cell.coord_x:
                        break

        return cells

    def check_path(self, path):
        """
        return cell if have step on path
        """
        states_count = 0
        next_player_state = PLAYERS_CELLS[self.next_player]
        current_player_state = PLAYERS_CELLS[self.current_player]

        for x, y in path:
            cell = self.board.coords(x, y)

            if cell.state != next_player_state and states_count == 0:
                break

            if cell.state != next_player_state and states_count > 0:
                return cell

            if cell.state == next_player_state:
                states_count += 1

    def get_next_cells(self):
        """
        mark all next step cells
        """
        current_player_state = PLAYERS_CELLS[self.current_player]
        next_player_state = PLAYERS_CELLS[self.next_player]

        for cell in self.board.cells[current_player_state]:
            for path in self.get_paths(cell):
                next_cell = self.check_path(path)

                if next_cell:
                    self.board.coords_state(next_cell.coord_x, next_cell.coord_y, CELL_STATE_STEP)

    def calculate_score(self):
        pass

    def toggle_player(self):
        self.current_player, self.next_player = self.next_player, self.current_player


class ReversiApp(App):
    def build(self):
        root = RootWidget()
        game = ReversiGame()
        game.compose(root)

        return root


if __name__ == '__main__':
    ReversiApp().run()
