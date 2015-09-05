import math

class Point(object):
    """
    This class holds a position in a 2D world and helps doing some math
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self, rect):
        if self.x < rect.x:
            return False
        elif self.x >= rect.width:
            return False
        elif self.y < rect.y:
            return False
        elif self.y >= rect.height:
            return False
        return True

    def manhattan_distance_to(self, point):
        return abs(point.x - self.x) + abs(point.y - self.y)

    def euclidean_distance_to(self, point):
        return math.sqrt((point.x - self.x)**2 + (point.y - self.y)**2)

    def as_tuple(self):
        return self.x, self.y

    def __str__(self):
        return "x:" + str(self.x) + \
               " y:" + str(self.y)

    def equals(self, other_point):
        return self.x == other_point.x and self.y == other_point.y
