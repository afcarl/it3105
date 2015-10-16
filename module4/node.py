from board import Board
from copy import deepcopy
from game import Game
import random


class Node(object):
    snake_cell_weights = [
        [10.0, 8.0, 7.0, 6.5],
        [0.5, 0.7, 1.0, 3.0],
        [-0.5, -1.5, -1.8, -2],
        [-3.8, -3.7, -3.5, -3]
    ]

    edgy_cell_weights = [
        [2.0, 2.0, 2.0, 2.0],
        [2.0, 1.0, 1.0, 2.0],
        [2.0, 1.0, 1.0, 2.0],
        [2.0, 2.0, 2.0, 2.0]
    ]

    cell_weights = [
        [1.0, 1.0, 1.0, 1.0],
        [1.0, 1.0, 1.0, 1.0],
        [1.0, 1.0, 1.0, 1.0],
        [1.0, 1.0, 1.0, 1.0]
    ]

    def __init__(self, board, parent=None, my_turn=True, depth=0):
        self.board = board
        self.parent = parent
        self.corner_indexes = (0, self.board.size - 1)
        self.my_turn = my_turn
        self.depth = depth
        self.expectimax_average_cache = None
        self.expectimax_max_cache = None

    def __repr__(self):
        return self.board.__repr__() + \
               ", h=" + str(self.get_heuristic()) + \
               ", exp_max=", str(self.expectimax_max_cache)

    def generate_children(self):
        possible_moves = self.board.get_possible_moves()

        children = []
        for direction in possible_moves:
            board_values_copy = deepcopy(self.board.board_values)
            child_board = Board()
            child_board.set_board_values(board_values_copy)
            child_board.move(direction)
            child = Node(board=child_board, parent=self, depth=self.depth)
            children.append(child)
        return children

    def get_cell_weight(self, row_index, column_index):
        return self.snake_cell_weights[row_index][column_index]

    def expectimax_max(self):
        if self.expectimax_max_cache is not None:
            return self.expectimax_max_cache

        children = self.generate_children()
        if len(children) == 0:
            return 0, None

        sorted_children = sorted(
            children,
            key=lambda child: child.expectimax_average(),
            reverse=True
        )
        self.expectimax_max_cache = sorted_children[0].expectimax_average()
        return self.expectimax_max_cache, sorted_children[0]

    def expectimax_average(self):
        if self.expectimax_average_cache is not None:
            return self.expectimax_average_cache
        empty_tiles = []
        for row_index in xrange(self.board.size):
            for column_index in xrange(self.board.size):
                cell_value = self.board.board_values[row_index][column_index]
                if cell_value == 0:
                    empty_tiles.append((row_index, column_index))

        total_expected_heuristic_value = 0

        values_to_try = [(2, 0.9)]  # , (4, 0.1)]  # don't consider new fours
        combinations = []

        for row_index, column_index in empty_tiles:
            for value, probability in values_to_try:
                combinations.append((row_index, column_index, value, probability))
        random.shuffle(combinations)

        # max branching factor is 4
        for row_index, column_index, value, probability in combinations[:4]:
            board_copy = deepcopy(self.board)
            board_copy.board_values[row_index][column_index] = value
            node = Node(board_copy, depth=self.depth + 1)
            if node.depth == 3:
                heuristic_value = node.get_heuristic()
            else:
                heuristic_value, best_child = node.expectimax_max()

            total_expected_heuristic_value += heuristic_value * probability

        self.expectimax_average_cache = float(total_expected_heuristic_value) / len(combinations)
        return self.expectimax_average_cache

    def get_heuristic(self):
        heuristic = 0
        num_empty_cells = self.board.get_num_empty_tiles()

        for row_index in xrange(self.board.size):
            for column_index in xrange(self.board.size):
                cell_value = self.board.board_values[row_index][column_index]
                if cell_value != 0:
                    cell_weight = self.get_cell_weight(row_index, column_index)
                    heuristic += cell_weight * cell_value
        # for row in self.board.board_values:
        #    pass

        heuristic += num_empty_cells ** 2

        return heuristic

    def get_monte_carlo_heuristic(self):
        child_play_score = 0
        for x in xrange(100):
            board_copy = deepcopy(self.board)
            node_copy = Node(board_copy)
            child_play_score += Game.play_game_randomly(start_node=node_copy)
        return child_play_score
