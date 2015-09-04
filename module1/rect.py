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
