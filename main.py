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


class BoardCell(Image):
    cell_state = OptionProperty('', options=CELL_STATES)

    def __init__(self, **kwargs):
        super(BoardCell, self).__init__(**kwargs)

        self.width = 128
        self.height = 128

    def on_cell_state(self, instance, value):
        if value == CELL_STATE_EMPTY:
            self.texture = TEXTURE_EMPTY
        elif value == CELL_STATE_WHITE:
            self.texture = TEXTURE_WHITE
        elif value == CELL_STATE_BLACK:
            self.texture = TEXTURE_BLACK

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            pass

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

class ReversiGame(BoxLayout):
    current_player = OptionProperty(PLAYER_WHITE, options=[PLAYER_WHITE, PLAYER_BLACK])

    def __init__(self, **kwargs):
        super(ReversiGame, self).__init__(**kwargs)

        self.orientation = 'vertical'

        self.board = Board()
        self.board.padding = 10

        for i in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                broad_cell = BoardCell()
                broad_cell.cell_state = 'empty'
                self.board.add_widget(broad_cell)

        self.add_widget(self.board)

        self.scores = Scores()
        self.scores.size_hint_y = 0.2

        self.player1 = Label(text='Player 1', size_hint_x=.4)
        self.player2 = Label(text='Player 2', size_hint_x=.4)
        self.btn_undo = Button(text='Undo', size_hint_x=.2)

        self.scores.add_widget(self.player1)
        self.scores.add_widget(self.btn_undo)
        self.scores.add_widget(self.player2)

        self.add_widget(self.scores)



class ReversiApp(App):
    def build(self):
        return ReversiGame()


if __name__ == '__main__':
    ReversiApp().run()
