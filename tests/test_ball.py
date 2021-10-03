from gamelib import Ball
import pyglet
import pymunk
from pymunk.vec2d import Vec2d
pymunk.init_pymunk()

def get_ball():
    return Ball((0, 0))

def fill_ball(ball):
    ball.to_batch(pyglet.graphics.Batch())
    ball.to_space(pymunk.Space())
    return ball

def test_ball():
    ball = get_ball()
    assert pyglet.sprite.Sprite is type(ball.sprite)

def test_to_batch():
    batch = pyglet.graphics.Batch()
    ball = get_ball()
    ball.to_batch(batch)
    assert batch is ball.sprite.batch

def test_to_space():
    ball = get_ball()
    assert not ball.shape
    space = pymunk.Space()
    n_shapes, n_bodies = len(space.shapes), len(space.bodies)
    ball.to_space(space)
    assert type(ball.shape) is pymunk.Circle
    assert n_shapes + 1 == len(space.shapes)
    assert n_bodies + 1 == len(space.bodies)

def test_get_position():
    ball = get_ball()
    assert list(ball.position) == list(ball.sprite.position)
    ball = fill_ball(ball)
    assert list(ball.position) == list(ball.shape.body.position)

def test_position_changed():
    ball = get_ball()
    space = pymunk.Space()
    ball.to_space(space)
    ball.shape.body.position.x = 10
    ball.shape.body.position.y = 20
    ball.position_changed()
    assert 10 == ball.sprite.x
    assert 20 == ball.sprite.y

def test_ball_kick():
    ball = fill_ball(get_ball())
    ball.shape.body.velocity = Vec2d(100.0, 0.0)
    velocity = list(ball.shape.body.velocity) # copy of velocity
    ball.kick(direction=Vec2d(1.0, 0.0), power=1.0)
    assert [100.0, 0.0] != list(ball.shape.body.velocity)

def test_is_out():
    b = Ball((0.0, -9.0))
    b.radius = 10.0
    assert not b.is_out()
    b = Ball((0.0, -21.0))
    b.radius = 20.0
    assert b.is_out()

