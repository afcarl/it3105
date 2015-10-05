from point import Point
from base_node import BaseNode


class Node(BaseNode):
    """
    This is a Node implementation that is specific to the "find shortest path" problem
    """
    H_MULTIPLIER = 1
    board = None

    def __init__(self, position, g=None, h=None, parent=None):
        super(Node, self).__init__(g=g, h=h, parent=parent)
        self.position = position

    def calculate_h(self):
        self.h = self.position.euclidean_distance_to(self.board.goal) * Node.H_MULTIPLIER

    def generate_children(self):
        children = set()
        candidate_positions = {
            Point(x=self.position.x, y=self.position.y + 1),
            Point(x=self.position.x, y=self.position.y - 1),
            Point(x=self.position.x + 1, y=self.position.y),
            Point(x=self.position.x - 1, y=self.position.y)
        }
        for position in candidate_positions:
            if self.board.is_tile_accessible(position):
                child = Node(position)
                children.add(child)
        return children

    def is_solution(self):
        return self.position.x == self.board.goal.x and self.position.y == self.board.goal.y

    def __eq__(self, other_node):
        return self.position.as_tuple() == other_node.position.as_tuple()

    def __hash__(self):
        return hash(self.position.as_tuple())

    def get_arc_cost(self, other_node):
        return Node.ARC_COST_MULTIPLIER

    def __str__(self):
        return "x:" + str(self.position.x) + \
               " y:" + str(self.position.y)
