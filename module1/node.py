from two_dee import Point


class Node:
    def __init__(self, board, position, g, h=None, parent=None):
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

    def get_children(self):
        children = set()
        candidates = {
            Point(self.position.x, self.position.y + 1),
            Point(self.position.x, self.position.y - 1),
            Point(self.position.x + 1, self.position.y),
            Point(self.position.x - 1, self.position.y)
        }
        for child in candidates:
            if self.board.is_tile_accessible(child):
                children.add(child)
        return children
