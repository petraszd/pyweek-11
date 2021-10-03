import pyglet
import pyglet.gl as gl
import pymunk
from pymunk.vec2d import Vec2d
from options import SEGMENT_WIDTH, SEGMENT_COLOR

__all__ = ["Segment"]

class Segment(object):
    def __init__(self, a, b):
        self.a = Vec2d(a)
        self.b = Vec2d(b)
        self.vertex_list = None
        self.shape = None

    def to_batch(self, batch):
        self.vertex_list = batch.add(2, gl.GL_LINES, None,
            ('v2i', map(int, list(self.a) + list(self.b))),
            ('c3B', SEGMENT_COLOR * 2)
        )

    def to_space(self, space):
        body = pymunk.Body(pymunk.inf, pymunk.inf)
        body.position = (0, 0)
        self.shape = pymunk.Segment(body, self.a, self.b, SEGMENT_WIDTH)
        space.add_static(self.shape)

