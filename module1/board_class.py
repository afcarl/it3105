class Board:
    TILE_STATES = {
        "NOT_ACCESSIBLE": -1,
        "UNEXPLORED": 0,
        "OPEN": 1,
        "CLOSED": 2,
        "ACTIVE": 3
    }

    def __init__(self, dimensions, start, goal):
        self.tiles = []
        for i in range(dimensions.height):
            self.tiles.append([])
            for j in range(dimensions.width):
                self.tiles[i].append(0)

        self.dimensions = dimensions
        self.start = start
        self.goal = goal

    def is_tile_accessible(self, point):
        if not point.is_inside(self.dimensions):
            return False
