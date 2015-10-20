from board import Board
from copy import deepcopy
import random
import math


class Node(object):
    gradient_weights_up = [
        [4.0, 4.0, 4.0, 4.0],
        [3.0, 3.0, 3.0, 3.0],
        [2.0, 2.0, 2.0, 2.0],
        [1.0, 1.0, 1.0, 1.0]
    ]
    gradient_weights_right = [
        [1.0, 2.0, 3.0, 4.0],
        [1.0, 2.0, 3.0, 4.0],
        [1.0, 2.0, 3.0, 4.0],
        [1.0, 2.0, 3.0, 4.0]
    ]
    gradient_weights_down = [
        [1.0, 1.0, 1.0, 1.0],
        [2.0, 2.0, 2.0, 2.0],
        [3.0, 3.0, 3.0, 3.0],
        [4.0, 4.0, 4.0, 4.0]
    ]
    gradient_weights_left = [
        [4.0, 3.0, 2.0, 1.0],
        [4.0, 3.0, 2.0, 1.0],
        [4.0, 3.0, 2.0, 1.0],
        [4.0, 3.0, 2.0, 1.0]
    ]
    max_branching_factor = 4
    max_depth = 3
    smoothness_cache = {}
    monotonicity_cache = {}
    row_weight_cache = [
        {},
        {},
        {},
        {}
    ]
    cell_weight_exponent = 1.3

    def __init__(self, board, depth=0):
        self.board = board
        self.corner_indexes = (0, self.board.size - 1)
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
            child_board = Board(size=4, board_values=board_values_copy)
            child_board.move(direction)
            child = Node(board=child_board, depth=self.depth)
            children.append(child)
        return children

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

        random.shuffle(empty_tiles)

        value, probability = 2, 0.9  # only consider twos
        for row_index, column_index in empty_tiles[:self.max_branching_factor]:
            board_copy = deepcopy(self.board)
            board_copy.board_values[row_index][column_index] = value
            node = Node(board_copy, depth=self.depth + 1)

            if node.depth >= Node.max_depth:
                heuristic_value = node.get_heuristic()
            else:
                heuristic_value, best_child = node.expectimax_max()

            total_expected_heuristic_value += heuristic_value * probability

        self.expectimax_average_cache = float(total_expected_heuristic_value) / len(empty_tiles)
        return self.expectimax_average_cache

    def get_row_weight(self, row_index):
        cells_tuple = tuple(self.board.board_values[row_index])
        if cells_tuple in self.row_weight_cache[row_index]:
            return self.row_weight_cache[row_index][cells_tuple]

        cell_weight_term_up = 0
        cell_weight_term_right = 0
        cell_weight_term_down = 0
        cell_weight_term_left = 0
        for col_index in xrange(self.board.size):
            cell_value = self.board.board_values[row_index][col_index]
            if cell_value != 0:
                cell_weight_term_up += \
                    self.gradient_weights_up[row_index][col_index] * \
                    (cell_value ** self.cell_weight_exponent)
                cell_weight_term_right += \
                    self.gradient_weights_right[row_index][col_index] * \
                    (cell_value ** self.cell_weight_exponent)
                cell_weight_term_down += \
                    self.gradient_weights_down[row_index][col_index] * \
                    (cell_value ** self.cell_weight_exponent)
                cell_weight_term_left += \
                    self.gradient_weights_left[row_index][col_index] * \
                    (cell_value ** self.cell_weight_exponent)

        result = (
            cell_weight_term_up,
            cell_weight_term_right,
            cell_weight_term_down,
            cell_weight_term_left
        )
        self.row_weight_cache[row_index][cells_tuple] = result
        return result

    def get_heuristic(self):
        cell_weight_term_up = 0
        cell_weight_term_right = 0
        cell_weight_term_down = 0
        cell_weight_term_left = 0
        for row_index in xrange(self.board.size):
            up, right, down, left = self.get_row_weight(row_index)
            cell_weight_term_up += up
            cell_weight_term_right += right
            cell_weight_term_down += down
            cell_weight_term_left += left

        cell_weight_term = max(
            cell_weight_term_up,
            cell_weight_term_right,
            cell_weight_term_down,
            cell_weight_term_left
        )
        num_empty_tiles, max_tile_value, tile_sum = self.board.get_tile_stats()
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

        heuristic = cell_weight_term + \
                    empty_cells_term + \
                    smoothness + \
                    monotonicity + \
                    max_tile_value

        return heuristic

    @staticmethod
    def calculate_smoothness(cells):
        cells_tuple = tuple(cells)
        if cells_tuple in Node.smoothness_cache:
            return Node.smoothness_cache[cells_tuple]

        score = 0
        last_value = cells[0]
        for i in range(1, len(cells)):
            if cells[i] == last_value:
                score += max(last_value, 4)
            last_value = cells[i]

        Node.smoothness_cache[cells_tuple] = score
        return score

    @staticmethod
    def calculate_monotonicity(cells):
        cells_tuple = tuple(cells)
        if cells_tuple in Node.monotonicity_cache:
            return Node.monotonicity_cache[cells_tuple]

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
        result = max(score_left, score_right)
        Node.monotonicity_cache[cells_tuple] = result
        return result
