import sys
from ast import literal_eval
from two_dee import Point, Rect
from node import Node
from board_class import Board

f = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin

lines = []
for line in f:
    lines.append(line.strip())

f.close()

dimensions_tuple = literal_eval(lines[0])
dimensions = Rect(0, 0, dimensions_tuple[0], dimensions_tuple[1])
start = Point(literal_eval(lines[1].split(' ')[0]))
goal = Point(literal_eval(lines[1].split(' ')[1]))
print dimensions_tuple, start, goal

board = Board(dimensions, start, goal)

open_list = []
closed_list = []
start_node = Node(board, position=start, g=0)
start_node.h = start_node.position.manhattan_distance_to(goal)
start_node.calculate_f()
open_list.append(start_node)

for num_iterations in range(50000000):
    if len(open_list) == 0:
        print 'failed to find a solution'
    current_node = open_list.pop()
    closed_list.append(current_node)
