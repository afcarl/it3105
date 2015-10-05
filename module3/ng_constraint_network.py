import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from module2.constraint_network import Variable, ConstraintNetwork, Constraint
import itertools


class VertexColorVariable(Variable):
    """
    Problem-specific (graph coloring) class
    """

    def __init__(self, i, x, y):
        super(VertexColorVariable, self).__init__(name=i, domain=None)
        self.x = x
        self.y = y


class NgConstraintNetwork(ConstraintNetwork):
    """
    Problem-specific class
    vertices: list of VertexColorVariable instances
    edges: list of tuples
    initial_domain: list of numbers that shall be put into each domain initially
    """

    def __init__(self, num_cols, num_rows, row_segments, col_segments):

        # TODO: calculate domains and constraints

        constraints = None
        domains = None

        super(NgConstraintNetwork, self).__init__(constraints=constraints, domains=domains)

    @staticmethod
    def get_start_index_domains(size, segments):
        num_segments = len(segments)
        min_start_indexes = []
        min_start_index = 0
        for i in range(len(segments)):
            min_start_indexes.append(min_start_index)
            min_start_index += segments[i] + 1

        start_index_domains = []
        for i in range(num_segments):
            min_start_index = min_start_indexes[i]
            domain = []
            num_remaining_segments = len(min_start_indexes) - i - 1
            remaining_segments_sum = sum(segments[i + 1:num_segments])
            own_size = segments[i]
            upper_bound = size - num_remaining_segments - remaining_segments_sum - own_size + 1
            for x in range(min_start_index, upper_bound):
                domain.append(x)
            start_index_domains.append(domain)
        return start_index_domains

    @staticmethod
    def get_possible_combinations(size, segments, start_index_domains):
        possible_combinations = []
        for start_indexes in itertools.product(*start_index_domains):
            values = [0] * size
            is_valid_combination = True
            for i in range(len(start_indexes)):
                start_index = start_indexes[i]
                if i > 0 and start_index <= start_indexes[i - 1] + segments[i - 1]:
                    is_valid_combination = False
                segment_size = segments[i]
                for j in range(segment_size):
                    values[start_index + j] = 1

            if is_valid_combination:
                possible_combinations.append(tuple(values))
        return possible_combinations
