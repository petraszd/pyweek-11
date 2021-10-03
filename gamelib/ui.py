from pymunk.vec2d import Vec2d
from pyglet.image import load
from gamelib.util import center_sprite
from pyglet.sprite import Sprite
from pyglet.text import Label
from gamelib.options import UI_BTN_SRC, \
                            UI_BTN_FONT, \
                            UI_MOVER_SRC, \
                            UI_POWER_FONT, \
                            UI_POWER_DELTA, \
                            WINDOW_W

__all__ = ["Ui", "Button", "Mover", "PowerControl"]

class Ui(object):
    def __init__(self):
        self.elements = []
        self.active_elem = None

    def add(self, elem):
        self.elements.append(elem)

    def to_batch(self, batch):
        for el in self.elements:
            el.to_batch(batch)

    def on_mouse_press(self, pos):
        for el in self.elements:
            if el.is_within(pos):
                self.active_elem = el
                return
        self.active_elem = None

    def on_mouse_drag(self, deltas):
        if self.active_elem:
            self.active_elem.moved(deltas)

    def on_mouse_release(self, pos):
        if not self.active_elem:
            return
        self.active_elem.clicked()
        self.active_elem = None


class UiElem(object):
    def clicked(self):
        pass

    def moved(self, deltas):
        pass

class Button(UiElem):
    def __init__(self, pos, text, callback):
        self.position = Vec2d(pos)
        self.text = text
        self.callback = callback

    def clicked(self):
        self.callback()

    def to_batch(self, batch):
        self.sprite = Sprite(load(UI_BTN_SRC), batch=batch)
        center_sprite(self.sprite)
        img = self.sprite.image
        w, h = img.width, img.height
        self.label = Label(
            text=self.text, batch=batch, width=w,
            anchor_x='center', anchor_y='center',
            font_size=UI_BTN_FONT
        )
        self.label.x, self.label.y = self.position
        self.sprite.position = self.position

    def is_within(self, pos):
        return self.position.get_distance(pos) < self.sprite.image.height

class Mover(UiElem):
    def __init__(self, basket, space):
        self.basket = basket
        self.space = space

    def to_batch(self, batch):
        self.sprite = center_sprite(
            Sprite(load(UI_MOVER_SRC), batch=batch), y=0
        )
        self.sprite.position = self.basket.position

    def is_within(self, pos):
        self_pos = self.sprite.position
        delta_y = pos.y - self_pos[1]
        delta_x = abs(pos.x - self_pos[0])
        return delta_y > 0 and \
               delta_y < self.sprite.image.height and \
               delta_x < self.sprite.image.width / 2

    def moved(self, deltas):
        deltas.y = 0
        new_pos = Vec2d(self.basket.position) + deltas
        if new_pos.x < 0 or new_pos.x > WINDOW_W:
            return
        self.basket.move(deltas, self.space)
        self.sprite.position = new_pos

class PowerControl(UiElem):
    def __init__(self, force):
        self.int_power = 0
        self.force = force

    def to_batch(self, batch):
        self.int_power = int(self.force.power * 100)
        self.label = Label(
            text="{0}%".format(self.int_power),
            batch=batch,
            font_size=UI_POWER_FONT,
            x=self.force.position.x + UI_POWER_DELTA,
            y=self.force.position.y,
            color=(190, 0, 0, 255)
        )

    def is_within(self, pos):
        return pos.get_distance(self.force.position) < UI_POWER_DELTA

    def moved(self, deltas):
        delta = deltas.y
        new_pow = self.int_power + int(delta)
        if new_pow < 0 or new_pow > 100:
            return

        self.label.text = "{0}%".format(new_pow)
        self.force.power = new_pow / 100.0
        self.int_power = new_pow

