from gamelib import Force, Ball
import pyglet
import pymunk
from pymunk.vec2d import Vec2d
import math
import py

def get_force():
    return Force(
        position=(1, 1),
        direction=(1, 1),
        power=0.5
    )

def get_ball():
    b = Ball((0.0, 0.0))
    b.radius = 40.0
    b.to_batch(pyglet.graphics.Batch())
    b.to_space(pymunk.Space())
    return b

def test_force():
    f = get_force()
    coord = 1.0 / math.sqrt(2)
    assert f.direction == [coord, coord]

def test_to_batch():
    f = get_force()
    b = pyglet.graphics.Batch()
    assert None is f.sprite
    f.to_batch(b)
    assert f.sprite

    assert f.sprite.x == f.position.x
    assert f.sprite.y == f.position.y
    assert f.sprite.rotation == f.direction.get_angle_degrees()

def test_is_ball_nearby():
    f = get_force()
    f.position = Vec2d(0.0, 0.0)
    b = get_ball()
    assert f.is_ball_nearby(b)
    f.position = Vec2d(46.0, 0.0)
    assert not f.is_ball_nearby(b)

def test_use():
    f = get_force()
    assert not f.used
    f.use(get_ball())
    assert f.used

