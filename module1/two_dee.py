import math

class Point(object):
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


class Rect:
    def __init__(self, x, y, width, height):
        if width < 0 or height < 0:
            raise Exception('negative width or height is not allowed')
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_border_tiles(self):
        tiles = set()
        for x in range(self.x, self.x + self.width):
            y = self.y
            tiles.add((x, y))
            y = self.y + self.height - 1
            tiles.add((x, y))
        for y in range(self.y + 1, self.y + self.height - 1):
            x = self.x
            tiles.add((x, y))
            x = self.x + self.width - 1
            tiles.add((x, y))
        return tiles

    def __str__(self):
        return "x:" + str(self.x) + \
               " y:" + str(self.y) + \
               " width:" + str(self.width) + \
               " height" + str(self.height)
