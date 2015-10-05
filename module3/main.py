import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import argparse
from module2.csp_node import CspNode
from ng_constraint_network import NgConstraintNetwork
import time
from module1.a_star import AStar
from module2.csp_node import CspNode
from copy import deepcopy


class Main(object):
    def __init__(self):
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
        arg_parser.add_argument(
            '--sleep-afterwards',
            nargs='?',
            dest='sleep_afterwards',
            help='At the end of the run, sleep for a couple of seconds. This gives you time to'
                 ' take a screenshot of the solution, for example',
            const=True,
            required=False,
            default=False
        )
        args = arg_parser.parse_args()
        self.sleep_afterwards = args.sleep_afterwards

        if args.mode == 'bfs':
            CspNode.H_MULTIPLIER = 0
        elif args.mode == 'dfs':
            CspNode.H_MULTIPLIER = 0
            CspNode.ARC_COST_MULTIPLIER = 0

        f = open(args.filename)
        lines = []
        for line in f:
            lines.append(line.strip())
        f.close()

        num_cols, num_rows, row_segments, col_segments = self.parse_lines(lines)

        # initialize constraint network
        self.constraint_network = NgConstraintNetwork(
            num_cols=num_cols,
            num_rows=num_rows,
            row_segments=row_segments,
            col_segments=col_segments
        )

        if not args.disable_gfx:
            from gfx import Gfx
            self.gfx = Gfx(grid_width=num_cols, grid_height=num_rows, fps=args.fps)

        self.a_star = AStar(
            draw=self.gfx.draw if not args.disable_gfx else lambda _: 0,
            disable_gfx=args.disable_gfx,
            draw_every=args.draw_every,
            print_path=args.print_path
        )

        if args.print_execution_time:
            self.start_time = time.time()

        self.run()

        if args.print_execution_time:
            print "execution time: %s seconds" % (time.time() - self.start_time)

    @staticmethod
    def parse_lines(lines):
        """
        Parse the lines of the input file according to the spec
        :param lines: array
        """
        num_cols, num_rows = map(int, lines[0].split(' '))

        row_segments = []
        # Read this backwards because we want to define y = 0 as the top, not the bottom
        for i in reversed(range(1, num_rows + 1)):
            segments = map(int, lines[i].split(' '))
            row_segments.append(segments)

        col_segments = []
        for i in range(num_rows + 1, num_rows + 1 + num_cols):
            segments = map(int, lines[i].split(' '))
            col_segments.append(segments)

        return num_cols, num_rows, row_segments, col_segments

    def run(self):
        CspNode.set_constraint_network(self.constraint_network)
        CspNode.set_constraints(self.constraint_network.constraints)
        start_node = CspNode(
            domains=deepcopy(self.constraint_network.domains),
            g=0
        )

        start_node.initialize_csp()
        start_node.domain_filtering()

        print 'running'
        self.a_star.run(start_node=start_node)
        if self.sleep_afterwards:
            time.sleep(5)

if __name__ == '__main__':
    Main()
