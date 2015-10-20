from board import Board
from node import Node
from game import Game
import argparse
import time


class Main(object):
    size = 4

    def __init__(self):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '--disable-gfx',
            nargs='?',
            dest='disable_gfx',
            const=True,
            required=False,
            default=False
        )
        arg_parser.add_argument(
            '--print-execution-time',
            nargs='?',
            dest='print_execution_time',
            help='At the end of the run, print the execution time',
            const=True,
            required=False,
            default=False
        )
        arg_parser.add_argument(
            '--max-depth',
            dest='max_depth',
            type=int,
            choices=[2, 3, 4],
            required=False,
            default=3
        )
        args = arg_parser.parse_args()

        if args.disable_gfx:
            from board_printer import BoardPrinter
            self.gfx = BoardPrinter()
        else:
            from gfx import Gfx
            self.gfx = Gfx(grid_width=self.size, grid_height=self.size, fps=30.0)

        Node.max_depth = args.max_depth

        if args.print_execution_time:
            self.start_time = time.time()

        self.run()

        if args.print_execution_time:
            print "execution time: %s seconds" % (time.time() - self.start_time)

    def run(self):
        board = Board(size=self.size)
        board.place_new_value_randomly()
        board.place_new_value_randomly()

        start_node = Node(board=board)
        print Game.play_game(start_node=start_node, gfx=self.gfx)

if __name__ == '__main__':
    Main()
