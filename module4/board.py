class Board(object):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __init__(self, size=4):
        self.size = size

        self.board = []
        for i in xrange(size):
            self.board.append([])
            for j in xrange(size):
                self.board[i].append(0)

    def can_move(self, direction):
        pass  # TODO

    def move(self, direction):
        pass  # TODO
