import sys
from ast import literal_eval
from rect import Rect
from point import Point
from node import Node
from board import Board
import argparse
import time
from a_star import AStar


class Main:
    def __init__(self):
        """
        Parse command line arguments, read input file, set up board and call run()
        """

        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '-i',
            '--input',
            dest='filename',
            type=str,
            help='The name of the input file',
            required=True
        )
        arg_parser.add_argument(
            '--mode',
            dest='mode',
            type=str,
            choices=['astar', 'bfs', 'dfs'],
            required=False,
            default="astar"
        )
        arg_parser.add_argument(
            '--fps',
            dest='fps',
            type=float,
            required=False,
            default=16.0
        )
        arg_parser.add_argument(
            '--draw-every',
            dest='draw_every',
            help='Use this argument to skip frames when visualizing large and complex problems',
            type=int,
            required=False,
            default=1
        )
        arg_parser.add_argument(
            '--disable-gfx',
            nargs='?',
            dest='disable_gfx',
            const=True,
            required=False,
            default=False
        )
        arg_parser.add_argument(
            '--print-path',
            nargs='?',
            dest='print_path',
            help='If a solution is found, print the backtracked nodes that led to the solution',
            const=True,
            required=False,
            default=False
        )
        arg_parser.add_argument(
            '--print-execution-time',
            nargs='?',
            dest='print_execution_time',
            help='At the end of the run, print the execution time of the A* algorithm. Useful for'
                 ' testing the performance of the algorithm while gfx is disabled.',
            const=True,
            required=False,
            default=False
        )
        args = arg_parser.parse_args()

        if args.mode == 'bfs':
            Node.H_MULTIPLIER = 0
        elif args.mode == 'dfs':
            Node.H_MULTIPLIER = 0
            Node.ARC_COST_MULTIPLIER = 0

        f = open(args.filename)
        lines = []
        for line in f:
            lines.append(line.strip())
        f.close()

        self.disable_gfx = args.disable_gfx
        self.print_path = args.print_path
        self.print_execution_time = args.print_execution_time
        self.draw_every = args.draw_every

        dimensions, start, goal, barriers = self.parse_lines(lines)
        self.board = Board(dimensions, start, goal, barriers)
        Node.board = self.board

        if not self.disable_gfx:
            from gfx import Gfx
            self.gfx = Gfx(board=self.board, fps=args.fps)

        if self.print_execution_time:
            self.start_time = time.time()
        self.run()
        if self.print_execution_time:
            print "execution time: %s seconds" % (time.time() - self.start_time)

    @staticmethod
    def parse_lines(lines):
        """
        Parse the lines of the input file according to the spec
        :param lines: array
        """
        dimensions_tuple = literal_eval(lines[0])
        dimensions = Rect(0, 0, dimensions_tuple[0], dimensions_tuple[1])
        start_tuple = literal_eval(lines[1].split(' ')[0])
        start = Point(x=start_tuple[0], y=start_tuple[1])
        goal_tuple = literal_eval(lines[1].split(' ')[1])
        goal = Point(x=goal_tuple[0], y=goal_tuple[1])
        barrier_tuples = lines[2:]
        barriers = []
        for barrier_tuple in barrier_tuples:
            barrier_tuple = literal_eval(barrier_tuple)
            barrier = Rect(*barrier_tuple)
            barriers.append(barrier)
        return dimensions, start, goal, barriers

    def run(self):
        start_node = Node(position=self.board.start, g=0)

        a_star = AStar(
            draw=self.gfx.draw if not self.disable_gfx else lambda _: 0,
            disable_gfx=self.disable_gfx,
            draw_every=self.draw_every,
            print_path=self.print_path
        )

        a_star.run(start_node=start_node)

if __name__ == '__main__':
    Main()
