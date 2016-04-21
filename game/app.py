# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.core.window import Window

from . import ReversiGame
from .config import *
from log import logger


Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)


class ReversiApp(App):
    def build(self):
        game = ReversiGame()
        root = game.get_root_widget()

        ReversiGame().compose(root)

        return root

