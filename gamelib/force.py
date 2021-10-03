import pyglet
from pymunk.vec2d import Vec2d
from pyglet.sprite import Sprite
from util import center_sprite
import math
from options import FORCE_IMG_SRC, \
                    FORCE_BASE_LEN, \
                    FORCE_DIST_DELTA

__all__ = ["Force"]

class Force(object):
    def __init__(self, position, direction, power=0.0):
        self.position = Vec2d(position)
        self.direction = Vec2d(direction).normalized()
        self.power = power
        self.sprite = None

        self.used = False

    def to_batch(self, batch):
        self.sprite = center_sprite(Sprite(
            pyglet.image.load(FORCE_IMG_SRC), batch=batch
        ), y=0)
        self.alter_sprite()

    def alter_sprite(self):
        degree = self.direction.get_angle_degrees()
        self.sprite.position = self.position
        self.sprite.rotation = degree

    def is_ball_nearby(self, ball):
        dist = self.position.get_distance(ball.position) - FORCE_DIST_DELTA
        return dist < ball.radius

    def use(self, ball):
        if self.used:
            return
        self.used = True
        ball.kick(self.direction, self.power)

