from pymunk.vec2d import Vec2d
from util import center_sprite
from pyglet.sprite import Sprite
from pyglet.image import load
from options import BASKET_IMG_SRC, \
                    BASKET_TOP_LEN, \
                    BASKET_BOTOOM_LEN, \
                    BASKET_HEIGHT, \
                    BASKET_DELTA
from segment import Segment

__all__ = ["Basket"]

class Basket(object):
    def __init__(self, position):
        self.position = Vec2d(position)
        self.sprite = None

    def to_batch(self, batch):
        self.sprite = center_sprite(Sprite(load(BASKET_IMG_SRC), batch=batch), y=2)
        self.sprite.position = self.position

    def to_space(self, space):
        p = self.position
        x1 = BASKET_BOTOOM_LEN / 2
        x2 = BASKET_TOP_LEN / 2
        h = BASKET_HEIGHT
        points = [
            ((p.x - x1, p.y), (p.x - x2, p.y + h)),
            ((p.x + x1, p.y), (p.x + x2, p.y + h)),
            ((p.x + x1, p.y), (p.x - x1, p.y)),
        ]
        self.segments = []
        for a, b in points:
            s = Segment(a, b)
            s.to_space(space)
            self.segments.append(s)

    def is_ball_in(self, ball):
        b_p = ball.position
        p = self.position
        return abs(p.y - b_p.y) - ball.radius < BASKET_DELTA and \
               abs(p.x - b_p.x) < BASKET_BOTOOM_LEN / 2

    def move(self, deltas, space):
        self.position += deltas
        self.sprite.position = self.position

        for s in self.segments:
            space.remove_static(s.shape)
            s.shape.a += deltas
            s.shape.b += deltas
            space.add_static(s.shape)

