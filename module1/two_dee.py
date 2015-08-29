class Point:
    def __init__(self, *args):
        if len(args) == 1:
            self.x = args[0][0]
            self.y = args[0][1]
        else:
            self.x = args[0]
            self.y = args[1]

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

    def __str__(self):
        return "x:" + str(self.x) + \
               " y:" + str(self.y)


class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self):
        return "x:" + str(self.x) + \
               " y:" + str(self.y) + \
               " width:" + str(self.width) + \
               " height" + str(self.height)
