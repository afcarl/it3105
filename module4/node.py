from board import Board
from copy import deepcopy
from game import Game


class Node(object):
    cell_weights = [
        [10.0, 8.0, 7.0, 6.5],
        [0.5, 0.7, 1.0, 3.0],
        [-0.5, -1.5, -1.8, -2],
        [-3.8, -3.7, -3.5, -3]
    ]

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
        """
        # gradient, collect greater values to the right
        factor = 1
        if row_index in self.corner_indexes and column_index in self.corner_indexes:
            factor = 4
        elif row_index in self.corner_indexes or column_index in self.corner_indexes:
            factor = 2
        return factor
        """

        return self.cell_weights[row_index][column_index]

    def get_heuristic(self):
        """
        heuristic = 0
        num_empty_cells = 0
        for row_index in xrange(self.board.size):
            for column_index in xrange(self.board.size):
                cell_value = self.board.board_values[row_index][column_index]
                if cell_value == 0:
                    num_empty_cells += 1
                else:
                    cell_weight = self.get_cell_weight(row_index, column_index)
                    heuristic += cell_weight * cell_value

        heuristic += num_empty_cells ** 2

        child_factor = 1.0

        children = self.generate_children()
        if len(children) == 0:
            return 0
        """

        child_play_score = 0

        for x in xrange(100):
            board_copy = deepcopy(self.board)
            node_copy = Node(board_copy)
            child_play_score += Game.play_game(start_node=node_copy, play_randomly=True)
        return child_play_score

        #return heuristic * child_factor
