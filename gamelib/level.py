import gamelib
from ui import Button, Ui, Mover, PowerControl
import pyglet
from pymunk import Space
from pyglet.graphics import Batch
from gamelib.options import SPACE_GRAVITY, \
                            LEVEL_SIM_SPEED, \
                            WINDOW_W, WINDOW_H

__all__ = ["Level"]

def pairs(l):
    return [l[i:i+2] for i, x in enumerate(l) if i % 2 == 0]

class Stage(object):
    def __init__(self, level):
        self.level = level

    def draw(self):
        pass

    def on_mouse_press(self, pos):
        pass

    def on_mouse_release(self, pos):
        pass

    def on_mouse_drag(self, deltas):
        pass

class BeforeStart(Stage):
    def draw(self):
        self.level.draw_game()
        self.level.draw_ui()

    def on_mouse_press(self, pos):
        self.level.ui.on_mouse_press(pos)

    def on_mouse_release(self, pos):
        self.level.ui.on_mouse_release(pos)

    def on_mouse_drag(self, deltas):
        self.level.ui.on_mouse_drag(deltas)

class AfterStart(Stage):
    def draw(self):
        self.level.draw_game()

class Level(object):
    def __init__(self, fileobj, win_fn, lose_fn):
        self.ball = None
        self.basket = None
        self.forces = []
        self.segments = []

        self.game_batch = Batch()
        self.ui_batch = Batch()

        self.space = Space()
        self.space.gravity = (0.0, SPACE_GRAVITY)

        self.need_mover = True
        self.read_from_file(fileobj)
        self.init_game_objects()
        self.ui = self.create_ui()

        self.stage = BeforeStart(self)

        self.win_callback = win_fn
        self.lose_callback = lose_fn

    def _do_nothing(self):
        pass

    def can_be_restarted(self):
        return True

    def read_from_file(self, f):
        for line in f.readlines():
            params = line.split()
            attr_name = params[0]
            if attr_name == "option" and len(params) > 1:
                self.set_option(params[1])
                continue

            cl_name = attr_name.capitalize()
            try:
                args = pairs([int(x) for x in params[1:]])
                cl = getattr(gamelib, cl_name)
                obj = cl(*args)
                if hasattr(self, attr_name):
                    setattr(self, attr_name, obj)
                else:
                    getattr(self, attr_name + "s").append(obj)
            except Exception as e: # bad formated input file
                continue

    def set_option(self, option):
        if option == "no_mover":
            self.need_mover = False

    def create_ui(self):
        ui = Ui()
        ui.add(Button((WINDOW_W / 2, WINDOW_H - 50), "Simulate", self.simulate))
        if self.need_mover:
            ui.add(Mover(self.basket, self.space))
        for f in self.forces:
            ui.add(PowerControl(f))
        ui.to_batch(self.ui_batch)
        return ui

    def draw(self):
        self.stage.draw()

    def draw_ui(self):
        self.ui_batch.draw()

    def draw_game(self):
        self.game_batch.draw()

    def init_game_objects(self):
        for obj in self.segments + [self.ball, self.basket]:
            obj.to_space(self.space)
            obj.to_batch(self.game_batch)
        for f in self.forces:
            f.to_batch(self.game_batch)

    def simulate(self):
        self.stage = AfterStart(self)
        pyglet.clock.schedule(self.on_tick)

    def register_win_callback(self, fn):
        self.win_callback = fn

    def register_lose_callback(self, fn):
        self.lose_callback = fn

    # Events
    def on_mouse_press(self, pos):
        self.stage.on_mouse_press(pos)

    def on_mouse_release(self, pos):
        self.stage.on_mouse_release(pos)

    def on_mouse_drag(self, deltas):
        self.stage.on_mouse_drag(deltas)

    def on_tick(self, dt):
        self.space.step(dt * LEVEL_SIM_SPEED)
        self.ball.position_changed()
        for f in self.forces:
            if f.is_ball_nearby(self.ball):
                f.use(self.ball)
        if self.basket.is_ball_in(self.ball):
            pyglet.clock.unschedule(self.on_tick)
            self.win_callback()
        elif self.ball.is_out():
            pyglet.clock.unschedule(self.on_tick)
            self.lose_callback()

