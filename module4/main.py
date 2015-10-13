from gfx import Gfx
from board import Board
import random
from node import Node


class Main(object):
    def __init__(self):
        size = 4
        self.gfx = Gfx(grid_width=size, grid_height=size, fps=30.0)
        board = Board(size=size)
        board.place_new_value_randomly()
        board.place_new_value_randomly()

        start_node = Node(board=board)
        current_node = start_node
        for x in xrange(10000):
            self.gfx.draw(current_node.board.board_values)

            children = current_node.generate_children()
            if len(children) == 0:
                print 'game over'
                print current_node.board
                break

            sorted_children = sorted(
                children,
                key=lambda child: child.get_heuristic(),
                reverse=True
            )
            current_node = sorted_children[0]
            current_node.board.place_new_value_randomly()

Main()
