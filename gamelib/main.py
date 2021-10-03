def run_game():
    import pyglet
    import pyglet.gl as gl
    import pymunk
    pymunk.init_pymunk()
    from pymunk.vec2d import Vec2d
    import random
    from gamelib import Game
    from gamelib.options import WINDOW_W, WINDOW_H, \
                                GAME_LEVELS_PATH, \
                                WINDOW_BACK_SRC


    def setup_gl():
        gl.glClearColor(0.7, 0.7, 0.7, 1.0)
        gl.glLineWidth(4.0)
        gl.glEnable(gl.GL_LINE_SMOOTH)
        gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST)

    window = pyglet.window.Window(width=WINDOW_W, height=WINDOW_H)
    game = Game(GAME_LEVELS_PATH)

    background = pyglet.sprite.Sprite(pyglet.image.load(WINDOW_BACK_SRC))

    @window.event
    def on_draw():
        window.clear()
        background.draw()
        game.draw()

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        game.on_mouse_press(Vec2d(x, y))

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        game.on_mouse_release(Vec2d(x, y))

    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        game.on_mouse_drag(Vec2d(dx, dy))

    @window.event
    def on_key_release(symbol, modifiers):
        key = pyglet.window.key
        if symbol == key.Q:
            pyglet.app.exit()

    setup_gl()
    game.hello_screen()
    pyglet.app.run()

