from two_dee import Point


class Node(Point):
    def __init__(self, board, position, g=None, h=None, parent=None):
        super(Node, self).__init__(position.x, position.y)
        self.board = board
        self.position = position
        self.parent = parent
        self.g = g
        self.h = h
        self.f = None

    def set_parent(self, parent):
        self.parent = parent

    def set_g(self, g):
        self.g = g

    def calculate_f(self):
        self.f = self.g + self.h

    def calculate_h(self):
        self.h = self.position.euclidean_distance_to(self.board.goal)

    def get_children(self):
        children = set()
        candidate_positions = {
            Point(self.position.x, self.position.y + 1),
            Point(self.position.x, self.position.y - 1),
            Point(self.position.x + 1, self.position.y),
            Point(self.position.x - 1, self.position.y)
        }
        for position in candidate_positions:
            if self.board.is_tile_accessible(position):
                child = Node(self.board, position, None, None, self)
                children.add(child)
        return children

    def is_solution(self):
        return self.equals(self.board.goal)

    def get_ancestors(self):
        ancestors = []
        current_node = self
        while True:
            if current_node.parent is None:
                return ancestors
            else:
                ancestors.append(current_node.parent)
                current_node = current_node.parent

    def __eq__(self, other_node):
        return self.as_tuple() == other_node.as_tuple()

    def __hash__(self):
        return hash(self.as_tuple())

    @staticmethod
    def get_arc_cost():
        return 1
