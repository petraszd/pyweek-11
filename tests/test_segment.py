from gamelib import Segment
import pyglet
import pymunk
pymunk.init_pymunk()

def get_segment():
    a = (0, 10)
    b = (0, 10)
    return Segment(a, b)

def test_segment():
    segment = get_segment()
    assert None is segment.vertex_list
    assert None is segment.shape

def test_to_batch():
    segment = get_segment()
    batch = pyglet.graphics.Batch()
    segment.to_batch(batch)
    VL = pyglet.graphics.vertexdomain.VertexList
    assert type(segment.vertex_list) is VL
    assert list(segment.vertex_list.vertices) == list(segment.a) + list(segment.b)

def test_to_space():
    space = pymunk.Space()
    segment = get_segment()
    n_bodies, n_shapes = len(space.static_shapes), len(space.bodies)
    segment.to_space(space)
    assert type(segment.shape) is pymunk.Segment
    assert n_bodies == len(space.bodies)
    assert n_shapes + 1 == len(space.static_shapes)

