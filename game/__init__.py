# -*- coding: utf-8 -*-

from .config import *
from .log import logger
from .ui import Board, BoardCell, Scores, RootWidget


class ReversiGame(object):
    instance = None

    def __new__(cls):
        if not cls.instance:
            cls.instance = super(ReversiGame, cls).__new__(cls)

        return cls.instance

    def get_root_widget(self):
        return RootWidget()

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
        self.scores.calculate_score()
        root.add_widget(self.scores)

        self.get_next_cells()

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
        """
        reset cells that show next steps
        """
        cells = [(i.coord_x, i.coord_y)for i in self.board.cells[CELL_STATE_STEP]]

        for x, y in cells:
            self.board.coords_state(x, y, CELL_STATE_EMPTY)

            logger.log('reset_next_cells: cell=%s' % self.board.coords(x, y))

    def get_win_cells(self, cell):
        win_cells = []

        for path in self.get_paths(cell):
            next_cell = self.check_path(path)

            if next_cell and next_cell.state == cell.state:
                for x, y in path:
                    win_cells.append(self.board.coords(x, y))

                    if next_cell.coord_x == x and next_cell.coord_x:
                        break

        logger.log('get_win_cells: cell=%s win_cells=%s' % (cell, win_cells))

        return win_cells

    def check_path(self, path):
        """
        return cell if have step on path
        """
        states_count = 0
        next_player_state = PLAYERS_CELLS[self.next_player]

        cell = None
        for x, y in path:
            cell = self.board.coords(x, y)

            if cell.state != next_player_state and states_count == 0:
                cell = None
                break

            if cell.state != next_player_state and states_count > 0:
                break

            if cell.state == next_player_state:
                states_count += 1

        logger.log('check_path: path=%s cell=%s' % (path, cell))

        return cell

    def get_next_cells(self):
        """
        mark all next step cells
        """
        self.reset_next_cells()

        current_player_state = PLAYERS_CELLS[self.current_player]
        result = []

        for cell in self.board.cells[current_player_state]:
            for path in self.get_paths(cell):
                next_cell = self.check_path(path)

                if next_cell and next_cell.state == CELL_STATE_EMPTY:
                    result.append(next_cell)
                    self.board.coords_state(next_cell.coord_x, next_cell.coord_y, CELL_STATE_STEP)

                    logger.log('get_next_cells: post - %s' % next_cell)

        return result

    def toggle_player(self):
        self.current_player, self.next_player = self.next_player, self.current_player

        self.scores.labels[self.current_player].bold = True
        self.scores.labels[self.next_player].bold = False

        logger.log('current_player=%s' % self.current_player)
