import sys
from ast import literal_eval
from rect import Rect
from point import Point
from node import Node
from board import Board
from gfx import Gfx
from priority_set import NodePrioritySet
import argparse
import time


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
        start = Point(*start_tuple)
        goal_tuple = literal_eval(lines[1].split(' ')[1])
        goal = Point(*goal_tuple)
        barrier_tuples = lines[2:]
        barriers = []
        for barrier_tuple in barrier_tuples:
            barrier_tuple = literal_eval(barrier_tuple)
            barrier = Rect(*barrier_tuple)
            barriers.append(barrier)
        return dimensions, start, goal, barriers

    def run(self):
        """
        Run the A* algorithm
        """
        open_list = NodePrioritySet()
        closed_list = {}
        start_node = Node(position=self.board.start, g=0)
        start_node.calculate_h()
        start_node.calculate_f()
        open_list.add(start_node, start_node.f)

        def attach_and_eval(parent_node, child_node):
            child_node.set_g(parent_node.g + parent_node.get_arc_cost(child_node))
            child_node.calculate_h()
            child_node.calculate_f()
            child_node.set_parent(parent_node)

        # If the algorithm still hasn't found a solution after the max number of iterations,
        # then the algorithm will stop
        max_num_iterations = 50000000
        for num_iterations in range(max_num_iterations):
            if open_list.is_empty():
                print 'Failed to find a solution'
                return False
            current_node = open_list.pop()
            closed_list[current_node] = current_node
            if not self.disable_gfx and num_iterations % self.draw_every == 0:
                ancestors = current_node.get_ancestors()
                self.gfx.draw(current_node, ancestors, closed_list, open_list)  # draw current state
            if current_node.is_solution():
                print "number of nodes created:", len(closed_list) + len(open_list.dict)
                ancestors = current_node.get_ancestors()
                print "path length:", len(ancestors)
                if self.print_path:
                    print "backtracked nodes that led to the solution:"
                    print current_node
                    for ancestor in ancestors:
                        print ancestor
                return current_node
            children = current_node.get_children()
            for child in children:
                previously_generated = False
                if child in open_list:
                    child = open_list[child]  # re-use previously generated node
                    previously_generated = True
                elif child in closed_list:
                    child = closed_list[child]  # re-use previously generated node
                    previously_generated = True

                if not previously_generated:
                    attach_and_eval(current_node, child)
                    open_list.add(child, child.f)
                elif current_node.g + current_node.get_arc_cost(child) < child.g:
                    attach_and_eval(current_node, child)

        print 'Failed to find a solution within the max number of iterations,', max_num_iterations
        return False


if __name__ == '__main__':
    Main()
