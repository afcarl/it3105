from board import Board
from copy import deepcopy
from game import Game
import random
import math


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

    gradient_cell_weights_up = [
        [4.0, 4.0, 4.0, 4.0],
        [3.0, 3.0, 3.0, 3.0],
        [2.0, 2.0, 2.0, 2.0],
        [1.0, 1.0, 1.0, 1.0]
    ]

    gradient_cell_weights_right = [
        [1.0, 2.0, 3.0, 4.0],
        [1.0, 2.0, 3.0, 4.0],
        [1.0, 2.0, 3.0, 4.0],
        [1.0, 2.0, 3.0, 4.0]
    ]

    gradient_cell_weights_down = [
        [1.0, 1.0, 1.0, 1.0],
        [2.0, 2.0, 2.0, 2.0],
        [3.0, 3.0, 3.0, 3.0],
        [4.0, 4.0, 4.0, 4.0]
    ]

    gradient_cell_weights_left = [
        [4.0, 3.0, 2.0, 1.0],
        [4.0, 3.0, 2.0, 1.0],
        [4.0, 3.0, 2.0, 1.0],
        [4.0, 3.0, 2.0, 1.0]
    ]

    cell_weights = [
        [1.0, 1.0, 1.0, 1.0],
        [1.0, 1.0, 1.0, 1.0],
        [1.0, 1.0, 1.0, 1.0],
        [1.0, 1.0, 1.0, 1.0]
    ]

    def __init__(self, board, depth=0, max_depth=3):
        self.board = board
        self.corner_indexes = (0, self.board.size - 1)
        self.depth = depth
        self.expectimax_average_cache = None
        self.expectimax_max_cache = None
        self.max_depth = max_depth

    def __repr__(self):
        return "node"
        return self.board.__repr__() + \
               ", h=" + str(self.get_heuristic()) + \
               ", exp_max=", str(self.expectimax_max_cache)

    def generate_children(self):
        possible_moves = self.board.get_possible_moves()

        children = []
        for direction in possible_moves:
            board_values_copy = deepcopy(self.board.board_values)
            child_board = Board(size=4, board_values=board_values_copy)
            child_board.move(direction)
            child = Node(board=child_board, depth=self.depth, max_depth=self.max_depth)
            children.append(child)
        return children

    def get_cell_weight(self, row_index, col_index):
        return max(
            self.gradient_cell_weights_up[row_index][col_index],
            self.gradient_cell_weights_right[row_index][col_index],
            self.gradient_cell_weights_down[row_index][col_index],
            self.gradient_cell_weights_left[row_index][col_index]
        )
        #return self.edgy_cell_weights[row_index][column_index]

    def expectimax_max(self, recalculate_max_depth=False):
        if self.expectimax_max_cache is not None:
            return self.expectimax_max_cache
        if recalculate_max_depth:
            num_empty_tiles, max_tile_value = self.board.get_tile_stats()
            if num_empty_tiles < 3 and max_tile_value >= 512:
                self.max_depth = 4
            else:
                self.max_depth = 3
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

        values_to_try = [(2, 0.9)]  # , (4, 0.1)]  # only consider twos
        combinations = []

        for row_index, column_index in empty_tiles:
            for value, probability in values_to_try:
                combinations.append((row_index, column_index, value, probability))
        random.shuffle(combinations)

        # max branching factor is 4
        for row_index, column_index, value, probability in combinations[:4]:
            board_copy = deepcopy(self.board)
            board_copy.board_values[row_index][column_index] = value
            node = Node(board_copy, depth=self.depth + 1, max_depth=self.max_depth)

            if node.depth >= node.max_depth:
                heuristic_value = node.get_heuristic()
            else:
                heuristic_value, best_child = node.expectimax_max()

            total_expected_heuristic_value += heuristic_value * probability

        self.expectimax_average_cache = float(total_expected_heuristic_value) / len(combinations)
        return self.expectimax_average_cache

    def get_heuristic(self):
        cell_weight_term_up = 0
        cell_weight_term_right = 0
        cell_weight_term_down = 0
        cell_weight_term_left = 0
        for row_index in xrange(self.board.size):
            for col_index in xrange(self.board.size):
                cell_value = self.board.board_values[row_index][col_index]
                if cell_value != 0:
                    exponent = 1.3
                    cell_weight_term_up += self.gradient_cell_weights_up[row_index][col_index] * (cell_value ** exponent)
                    cell_weight_term_right += self.gradient_cell_weights_right[row_index][col_index] * (cell_value ** exponent)
                    cell_weight_term_down += self.gradient_cell_weights_down[row_index][col_index] * (cell_value ** exponent)
                    cell_weight_term_left += self.gradient_cell_weights_left[row_index][col_index] * (cell_value ** exponent)

        cell_weight_term = max(
            cell_weight_term_up,
            cell_weight_term_right,
            cell_weight_term_down,
            cell_weight_term_left
        )
        num_empty_tiles, max_tile_value = self.board.get_tile_stats()
        empty_cells_term = 0.05 * max_tile_value * (num_empty_tiles ** 2)

        smoothness = 0
        monotonicity = 0
        for row in self.board.board_values:
            smoothness += self.calculate_smoothness(row)
            monotonicity += self.calculate_monotonicity(row)
        for col_index in range(self.board.size):
            col = self.board.get_column(col_index)
            smoothness += self.calculate_smoothness(col)
            monotonicity += self.calculate_monotonicity(col)

        #print 'cell_weight:', cell_weight_term, 'empty_cells:', empty_cells_term, 'smoothness:', smoothness, 'monotonicity:', monotonicity
        heuristic = cell_weight_term + \
                    empty_cells_term + \
                    smoothness + \
                    monotonicity + \
                    max_tile_value

        return heuristic

    @staticmethod
    def calculate_smoothness(cells):
        score = 0
        last_value = cells[0]
        for i in range(1, len(cells)):
            if cells[i] == last_value:
                score += max(last_value, 4)
            last_value = cells[i]
        return score

    @staticmethod
    def calculate_monotonicity(cells):
        score_right = 0
        score_left = 0
        last_value = cells[0]
        for i in range(1, len(cells)):
            log2_current = (math.log(cells[i], 2) if cells[i] > 0 else 0)
            log2_last = (math.log(last_value, 2) if last_value > 0 else 0)
            log2_diff = log2_current - log2_last
            score_added = (cells[i] + last_value) / (abs(log2_diff) + 1)
            if log2_diff > 0:
                score_right += score_added
                score_left -= score_added
            elif cells[i] < last_value:
                score_left += score_added
                score_right -= score_added
            last_value = cells[i]
        return max(score_left, score_right)

    def get_monte_carlo_heuristic(self):
        child_play_score = 0
        for x in xrange(100):
            board_copy = deepcopy(self.board)
            node_copy = Node(board_copy)
            child_play_score += Game.play_game_randomly(start_node=node_copy)
        return child_play_score
