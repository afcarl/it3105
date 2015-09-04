import sys
from ast import literal_eval
from two_dee import Point, Rect
from node import Node
from board import Board
from gfx import Gfx
from priority_set import NodePrioritySet


class Main:
    def __init__(self):
        f = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
        lines = []
        for line in f:
            lines.append(line.strip())
        f.close()

        dimensions, start, goal, barriers = self.parse_lines(lines)
        self.board = Board(dimensions, start, goal, barriers)

        self.gfx = Gfx(self.board)

        result = self.run()
        print 'result', result

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
        start_node = Node(self.board, position=self.board.start, g=0)
        start_node.calculate_h()
        start_node.calculate_f()
        open_list.add(start_node, start_node.h)

        max_num_iterations = 50000000
        for num_iterations in range(max_num_iterations):
            if open_list.is_empty():
                return False  # Fail
            current_node = open_list.pop()
            closed_list[current_node] = current_node
            if current_node.is_solution():
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
                    child.set_g(current_node.g + child.get_arc_cost())
                    child.calculate_h()
                    child.calculate_f()
                    child.set_parent(current_node)
                    open_list.add(child, child.f)
                elif False and True:  # TODO
                    pass  # TODO

            self.gfx.draw(current_node)

if __name__ == '__main__':
    Main()
