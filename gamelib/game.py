from pyglet.graphics import Batch
from pyglet.text import Label
import pyglet
from gamelib import Level
from gamelib.ui import Ui, Button
from gamelib.options import WINDOW_H, WINDOW_W
import os
import os.path

__all__ = ["Game"]

class Screen(object):
    def can_be_restarted(self):
        return False

    def on_mouse_press(self, pos):
        pass

    def on_mouse_release(self, pos):
        pass

    def on_mouse_drag(self, deltas):
        pass

    def draw(self):
        self.batch.draw()


class StartScreen(Screen):
    def __init__(self, start_game_fn):
        self.batch = Batch()

        self.ui = Ui()
        self.ui.add(Button(
            (WINDOW_W / 2, WINDOW_H / 2),
            "Start Game",
            start_game_fn
        ))
        self.ui.to_batch(self.batch)

    def on_mouse_press(self, pos):
        self.ui.on_mouse_press(pos)

    def on_mouse_release(self, pos):
        self.ui.on_mouse_release(pos)

    def on_mouse_drag(self, deltas):
        self.ui.on_mouse_drag(deltas)


class EndScreen(Screen):
    def __init__(self):
        self.batch = Batch()
        self.label = Label(
            "Congratulations!",
            x=WINDOW_W / 2, y=WINDOW_H / 2,
            width=WINDOW_W,
            halign="center",
            anchor_x="center",
            anchor_y="baseline",
            batch=self.batch,
            font_size=50
        )


class Game(object):
    def __init__(self, levels_path):
        self.levels = []
        self.active_item= None
        self.level_number = 0
        self.read_levels(levels_path)


    def read_levels(self, levels_path):
        self.levels = [os.path.join(levels_path, x) \
                       for x in sorted(os.listdir(levels_path))]

    def on_mouse_press(self, pos):
        if self.active_item:
            self.active_item.on_mouse_press(pos)

    def on_mouse_release(self, pos):
        if self.active_item:
            self.active_item.on_mouse_release(pos)

    def on_mouse_drag(self, deltas):
        if self.active_item:
            self.active_item.on_mouse_drag(deltas)

    def draw(self):
        if self.active_item:
            self.active_item.draw()

    def hello_screen(self):
        self.active_item = StartScreen(self.first_level)

    def end_screen(self):
        self.active_item = EndScreen()

    def first_level(self):
        self.level_number = 0
        self.start_level()

    def start_level(self):
        with open(self.levels[self.level_number], "r") as f:
            self.active_item = Level(f, self.next_level, self.restart_level)

    def restart_level(self):
        self.start_level()

    def next_level(self):
        self.level_number += 1
        if self.level_number >= len(self.levels):
            self.end_screen()
        else:
            self.start_level()

