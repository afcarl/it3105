class BaseNode(object):
    """
    This class represents the state of a node along with its score (f, g, h) and expand function
    This is the class that should be replaced or subclassed to implement other A* problems
    """
    ARC_COST_MULTIPLIER = 1

    def __init__(self, **kwargs):
        self.parent = kwargs.get("parent", None)
        self.g = kwargs.get("g", None)
        self.h = kwargs.get("h", None)
        self.f = None

    def set_parent(self, parent):
        self.parent = parent

    def set_g(self, g):
        self.g = g

    def calculate_f(self):
        self.f = self.g + self.h

    def calculate_h(self):
        pass  # must be implemented

    def generate_children(self):
        pass  # must be implemented

    def is_solution(self):
        pass  # must be implemented

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
        pass  # must be implemented

    def __hash__(self):
        pass  # must be implemented

    def get_arc_cost(self, other_node):
        return self.ARC_COST_MULTIPLIER
