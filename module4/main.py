from gfx import Gfx
from board import Board
import random


class Main(object):
    def __init__(self):
        size = 4
        self.gfx = Gfx(grid_width=size, grid_height=size, fps=8.0)
        self.board = Board(size=size)
        self.board.place_new_value_randomly()
        self.board.place_new_value_randomly()

        for x in xrange(10000):
            self.gfx.draw(self.board.board_values)
            moves = self.board.get_possible_moves()
            if len(moves) == 0:
                print 'game over'
                print self.board
                break

            direction = random.choice(moves)
            self.board.move(direction)
            self.board.place_new_value_randomly()

Main()
