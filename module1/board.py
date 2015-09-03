class Board:
    TILE_STATES = {
        "NOT_ACCESSIBLE": -1,
        "UNEXPLORED": 0,
        "OPEN": 1,
        "CLOSED": 2,
        "ACTIVE": 3
    }

    def __init__(self, dimensions, start, goal, barriers):
        self.tiles = []
        for i in range(dimensions.height):
            self.tiles.append([])
            for j in range(dimensions.width):
                self.tiles[i].append(0)

        self.rect = dimensions
        self.start = start
        self.goal = goal
        self.inaccessible_tiles = set()
        for barrier in barriers:
            self.inaccessible_tiles |= barrier.get_border_tiles()

    def is_tile_accessible(self, point):
        if point.as_tuple() in self.inaccessible_tiles or not point.is_inside(self.rect):
            return False
        return True
