import sys
from ast import literal_eval
from two_dee import Point, Rect
from node import Node
from board import Board
from gfx import Gfx
from priority_set import NodePrioritySet
import argparse


class Main:
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
            '-m',
            '--mode',
            dest='mode',
            type=str,
            choices=['astar', 'bfs', 'dfs'],
            required=False,
            default="astar"
        )
        args = arg_parser.parse_args()

        if args.mode == 'bfs':
            Node.H_MULTIPLIER = 0
        elif args.mode == 'dfs':
            Node.H_MULTIPLIER = 0
            Node.ARC_COST_MULTIPLIER = -1

        f = open(args.filename)
        lines = []
        for line in f:
            lines.append(line.strip())
        f.close()

        dimensions, start, goal, barriers = self.parse_lines(lines)
        self.board = Board(dimensions, start, goal, barriers)
        Node.board = self.board

        self.gfx = Gfx(self.board)

        self.run()

    @staticmethod
    def parse_lines(lines):
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
        open_list = NodePrioritySet()
        closed_list = {}
        start_node = Node(position=self.board.start, g=0)
        start_node.calculate_h()
        start_node.calculate_f()
        open_list.add(start_node, start_node.f)

        def attach_and_eval(current_node, child):
            child.set_g(current_node.g + current_node.get_arc_cost(child))
            child.calculate_h()
            child.calculate_f()
            child.set_parent(current_node)

        max_num_iterations = 50000000
        for num_iterations in range(max_num_iterations):
            if open_list.is_empty():
                print 'Failed to find a solution'
                return False
            current_node = open_list.pop()
            closed_list[current_node] = current_node
            self.gfx.draw(current_node, closed_list, open_list)
            if current_node.is_solution():
                print "number of iterations:", num_iterations
                ancestors = current_node.get_ancestors()
                print "path length:", len(ancestors)
                """
                print "backtracked path:"
                print current_node
                for ancestor in ancestors:
                    print ancestor
                """
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
