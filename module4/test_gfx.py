import unittest
from time import sleep
from gfx import Gfx


class TestMain(unittest.TestCase):
    def test_gfx(self):
        board = [
            [None, 8, 16, 2048],
            [None, 4, 32, 1024],
            [8192, 2, 64, 512],
            [4096, None, 128, 256]
        ]
        size = 4
        gfx = Gfx(size, size, fps=4)
        gfx.draw(board)
        sleep(2)

if __name__ == '__main__':
    unittest.main()
