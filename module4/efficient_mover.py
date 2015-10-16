from board import Board
import cPickle
from copy import deepcopy


class EfficientMover(object):
    def __init__(self):
        self.left_moves, self.right_moves = self.fetch_moves()

    def fetch_moves(self):
        file_name = "moves.pickle"
        try:
            moves = cPickle.load(open(file_name, "rb"))
        except IOError:
            moves = self.generate_moves()
            cPickle.dump(moves, open(file_name, "wb"))
        return moves

    @staticmethod
    def generate_moves():
        size = 4
        board = Board(size=size)

        left_moves = []
        right_moves = []

        num_combinations = 2 ** (size * size)

        for i in range(num_combinations):
            row = board.convert_integer_to_cells(i)
            board.board_values[0] = deepcopy(row)
            board.move_left()
            row_moved_left_as_int = board.convert_cells_to_integer(board.board_values[0])
            left_moves.append(row_moved_left_as_int)

            board.board_values[1] = deepcopy(row)
            board.move_right()
            row_moved_right_as_int = board.convert_cells_to_integer(board.board_values[1])
            right_moves.append(row_moved_right_as_int)

        return left_moves, right_moves

    def can_move_left(self, cells_integer):
        return cells_integer != self.left_moves[cells_integer]

    def can_move_right(self, cells_integer):
        return cells_integer != self.right_moves[cells_integer]

    def move_left(self, cells_integer):
        return self.left_moves[cells_integer]

    def move_right(self, cells_integer):
        return self.right_moves[cells_integer]

if __name__ == '__main__':
    EfficientMover()
