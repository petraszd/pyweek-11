from pyglet.image import load
from pyglet.sprite import Sprite
from gamelib.util import center_sprite
import pymunk
from pymunk.vec2d import Vec2d
from options import BALL_MASS, BALL_IMG_SRC, BALL_POWER, BALL_RADIUS

__all__ = ["Ball"]

class Ball(object):
    def __init__(self, pos):
        self.radius = BALL_RADIUS

        self.sprite = center_sprite(Sprite(load(BALL_IMG_SRC)))

        self.sprite.set_position(*pos)
        self.shape = None

    def to_batch(self, batch):
        self.sprite.batch = batch

    def to_space(self, space):
        r = self.radius
        inertia = pymunk.moment_for_circle(BALL_MASS, 0, r)
        body = pymunk.Body(BALL_MASS, inertia)
        body.position = self.sprite.position
        self.shape = pymunk.Circle(body, r)
        space.add(body, self.shape)

    def position_changed(self):
        self.sprite.set_position(*self.shape.body.position)
        #self.sprite.rotation += 2

    def kick(self, direction, power):
        # Bad, bad code...
        body = self.shape.body
        vel = body.velocity
        degree = 90.0
        if direction.y < 0.0:
            degree *= -1
        body.velocity = vel * (1.0 - power) + \
                        vel.rotated_degrees(degree) * power * BALL_POWER

    def is_out(self):
        return self.position.y + self.radius < 0.0

    @property
    def position(self):
        try:
            return self.shape.body.position
        except AttributeError:
            return Vec2d(list(self.sprite.position))

