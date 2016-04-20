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
TEXTURE_EMPTY = Image(source='empty.png').texture
TEXTURE_BLACK = Image(source='black.png').texture
TEXTURE_WHITE = Image(source='white.png').texture

CELL_STATE_WHITE = 'white'
CELL_STATE_BLACK = 'black'
CELL_STATE_EMPTY = 'empty'
CELL_STATES = [CELL_STATE_WHITE, CELL_STATE_BLACK, CELL_STATE_EMPTY]

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

    def execute(self):
        game = ReversiGame()
        game.toggle_player()
        self.cell.state = PLAYERS_CELLS[game.current_player]

        HISTORY.append(self)

    def cancel(self):
        game = ReversiGame()
        game.toggle_player()
        self.cell.state = CELL_STATE_EMPTY


class BoardCell(Image):
    state = OptionProperty(CELL_STATE_EMPTY, options=CELL_STATES)

    def __init__(self, **kwargs):
        super(BoardCell, self).__init__(**kwargs)

        self.coord_x = kwargs.get('coord_x', 0)
        self.coord_y = kwargs.get('coord_y', 0)

        self.width = 128
        self.height = 128

        self.texture = TEXTURE_EMPTY

    def get_coords(self):
        return self.coord_x, self.coord_y

    def on_state(self, instance, value):
        if value == CELL_STATE_EMPTY:
            self.texture = TEXTURE_EMPTY
        elif value == CELL_STATE_WHITE:
            self.texture = TEXTURE_WHITE
        elif value == CELL_STATE_BLACK:
            self.texture = TEXTURE_BLACK

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            command = MakeMoveCommand(self)
            command.execute()


class Board(GridLayout):
    def coords(self, x, y):
        return self.children[(x - 1) + BOARD_SIZE*(y - 1)]

    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)

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

        self.board = Board()
        self.board.padding = 10

        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                broad_cell = BoardCell(coord_x=x+1, coord_y=y+1)
                self.board.add_widget(broad_cell)

        self.board.coords(BOARD_SIZE/2, BOARD_SIZE/2).state = CELL_STATE_WHITE
        self.board.coords(BOARD_SIZE/2 + 1, BOARD_SIZE/2 + 1).state = CELL_STATE_WHITE
        self.board.coords(BOARD_SIZE/2, BOARD_SIZE/2 + 1).state = CELL_STATE_BLACK
        self.board.coords(BOARD_SIZE/2 + 1, BOARD_SIZE/2).state = CELL_STATE_BLACK

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

    def undo_handler(self, instance):
        command = UndoCommand()
        command.execute()

    def calculate_score(self):
        pass

    def toggle_player(self):
        if self.current_player == PLAYER_WHITE:
            self.current_player = PLAYER_BLACK
        else:
            self.current_player = PLAYER_WHITE


class ReversiApp(App):
    def build(self):
        root = RootWidget()
        game = ReversiGame()
        game.compose(root)

        return root


if __name__ == '__main__':
    ReversiApp().run()
