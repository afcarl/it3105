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
        north = Point(self.position.x, self.position.y + 1)
        south = Point(self.position.x, self.position.y - 1)
        east = Point(self.position.x + 1, self.position.y)
        west = Point(self.position.x - 1, self.position.y)
        #if north.is_inside(self.board.dimensions):

