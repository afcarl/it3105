from board import Board
from node import Node
from game import Game
import argparse


class Main(object):
    def __init__(self):
        size = 4

        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '--disable-gfx',
            nargs='?',
            dest='disable_gfx',
            const=True,
            required=False,
            default=False
        )
        args = arg_parser.parse_args()

        if args.disable_gfx:
            from board_printer import BoardPrinter
            self.gfx = BoardPrinter()
        else:
            from gfx import Gfx
            self.gfx = Gfx(grid_width=size, grid_height=size, fps=30.0)

        board = Board(size=size)
        board.place_new_value_randomly()
        board.place_new_value_randomly()

        start_node = Node(board=board)
        print Game.play_game(start_node=start_node, gfx=self.gfx)

if __name__ == '__main__':
    Main()
