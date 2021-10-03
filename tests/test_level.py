from gamelib import Level, Ball, Basket

class FileMock():
    def readlines(self):
        return [
            "ball 10 20\n",
            "segment 0 10 30 10\n",
            "segment 30 10 60 10\n",
            "basket 50 0\n",
            "force 20 30 5 4\n"
        ]

def win_callback():
    pass

def end_callback():
    pass

def test_level():
    level = Level(FileMock(), win_callback, end_callback)

    assert level.game_batch
    assert level.ui_batch

    assert level.space

    assert level.win_callback is win_callback
    assert level.lose_callback is end_callback

def test_read_from_file():
    level = Level(FileMock(), win_callback, end_callback)
    assert type(level.ball) == Ball
    assert type(level.basket) == Basket
    assert len(level.segments) == 2
    assert len(level.forces) == 1

def test_init_game_objects():
    level = Level(FileMock(), win_callback, end_callback)
    assert 1 == len(level.space.shapes)
    assert 5 == len(level.space.static_shapes)

