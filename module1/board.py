class Board:
    """
    This class holds information about the board, i.e. the size and the
    location of start, goal and barriers
    """

    def __init__(self, dimensions, start, goal, barriers):
        self.tiles = []
        for i in xrange(dimensions.height):
            self.tiles.append([])
            for j in xrange(dimensions.width):
                self.tiles[i].append(0)

        self.rect = dimensions
        self.start = start
        self.goal = goal
        self.barriers = barriers
        self.inaccessible_tiles = set()
        for barrier in barriers:
            self.inaccessible_tiles |= barrier.get_border_tiles()

    def is_tile_accessible(self, point):
        if point.as_tuple() in self.inaccessible_tiles or not point.is_inside(self.rect):
            return False
        return True
