import sys
from ast import literal_eval
from two_dee import Point, Rect
from node import Node
from board import Board

class Main:
    def __init__(self):
        f = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
        lines = []
        for line in f:
            lines.append(line.strip())
        f.close()

        dimensions, start, goal, barriers = self.parse_lines(lines)
        self.board = Board(dimensions, start, goal, barriers)

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
        open_list = []
        closed_list = []
        start_node = Node(self.board, position=self.board.start, g=0)
        start_node.h = start_node.position.manhattan_distance_to(self.board.goal)
        start_node.calculate_f()
        open_list.append(start_node)

        for num_iterations in range(50000000):
            if len(open_list) == 0:
                return False  # Fail
            current_node = open_list.pop()
            closed_list.append(current_node)

if __name__ == '__main__':
    Main()
