import pyglet
from gamelib import Basket, Ball
import pymunk
from pymunk.vec2d import Vec2d

def test_basket():
    basket = Basket(position=(10, 20))
    assert type(basket.position) == Vec2d

def test_to_batch():
    basket = Basket((50, 5))
    assert basket.sprite is None
    batch = pyglet.graphics.Batch()
    basket.to_batch(batch)
    assert type(basket.sprite) is pyglet.sprite.Sprite
    assert basket.sprite.batch is batch
    assert list(basket.sprite.position) == [50, 5]

def test_to_space():
    basket = Basket((0.0, 0.0))
    space = pymunk.Space()
    n_shapes = len(space.static_shapes)
    basket.to_space(space)
    assert n_shapes + 3 == len(space.static_shapes)

def test_is_ball_in():
    ball = Ball((40.0, 10.0))
    ball.radius = 10.0
    basket = Basket((100.0, 20.0))
    assert not basket.is_ball_in(ball)
    ball = Ball((100.0, 31.0))
    ball.radius = 10.0
    assert basket.is_ball_in(ball)

