from board import Board
from copy import deepcopy
from math import log


def log2(number):
    return log(number, 2) if number > 0 else 0


class Node(object):
    def __init__(self, board, parent=None):
        self.board = board
        self.parent = parent
        self.corner_indexes = (0, self.board.size - 1)

    def generate_children(self):
        possible_moves = self.board.get_possible_moves()

        children = []
        for direction in possible_moves:
            board_values_copy = deepcopy(self.board.board_values)
            child_board = Board()
            child_board.set_board_values(board_values_copy)
            child_board.move(direction)
            child = Node(board=child_board, parent=self)
            children.append(child)
        return children

    def get_cell_weight(self, row_index, column_index):
        # gradient, collect greater values to the right
        factor = 1
        if row_index in self.corner_indexes and column_index in self.corner_indexes:
            factor = 4
        elif row_index in self.corner_indexes or column_index in self.corner_indexes:
            factor = 2
        return factor

    def get_heuristic(self):
        dat_sum = 0
        values_map = {}
        for row_index in xrange(self.board.size):
            for column_index in xrange(self.board.size):
                cell_value = self.board.board_values[row_index][column_index]
                if cell_value in values_map:
                    values_map[cell_value] += 1
                else:
                    values_map[cell_value] = 1

                value_log = log2(cell_value)
                cell_weight = self.get_cell_weight(row_index, column_index)
                factor = 1.0

                if row_index + 1 < self.board.size:
                    other_value_log = log2(self.board.board_values[row_index + 1][column_index])
                    diff = abs(value_log - other_value_log)
                    if diff > 2:
                        factor /= 0.5 * diff
                if row_index - 1 >= 0:
                    other_value_log = log2(self.board.board_values[row_index - 1][column_index])
                    diff = abs(value_log - other_value_log)
                    if diff > 2:
                        factor /= 0.5 * diff

                if column_index + 1 < self.board.size:
                    other_value_log = log2(self.board.board_values[row_index][column_index + 1])
                    diff = abs(value_log - other_value_log)
                    if diff > 2:
                        factor /= 0.5 * diff
                if column_index - 1 >= 0:
                    other_value_log = log2(self.board.board_values[row_index][column_index - 1])
                    diff = abs(value_log - other_value_log)
                    if diff > 2:
                        factor /= 0.5 * diff

                dat_sum += factor * ((cell_weight * cell_value) ** 2)

        num_possible_moves = len(self.board.get_possible_moves())
        possible_moves_factor = 0.1 if num_possible_moves < 2 else 1
        if num_possible_moves == 0:
            possible_moves_factor = 0

        return dat_sum * possible_moves_factor
