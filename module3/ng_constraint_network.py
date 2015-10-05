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
        domains = {}

        # calculate and add column domains
        for col_index in range(len(col_segments)):
            start_index_domains = NgConstraintNetwork.get_start_index_domains(
                num_rows,
                col_segments[col_index]
            )
            possible_combinations = NgConstraintNetwork.get_possible_combinations(
                num_rows,
                col_segments[col_index],
                start_index_domains
            )

            col_key = "c" + str(col_index)
            domains[col_key] = possible_combinations

        # calculate and add row domains
        for row_index in range(len(row_segments)):
            start_index_domains = NgConstraintNetwork.get_start_index_domains(
                num_cols,
                row_segments[row_index]
            )
            possible_combinations = NgConstraintNetwork.get_possible_combinations(
                num_cols,
                row_segments[row_index],
                start_index_domains
            )

            row_key = "r" + str(row_index)
            domains[row_key] = possible_combinations

        # Calculate constraints. One for each cell
        constraints = {}
        for i in range(num_rows):
            for j in range(num_cols):
                constraint_variables = ('r' + str(i), 'c' + str(j))
                constraint_expression = "{}[{}] == {}[{}]".format(
                    constraint_variables[0],
                    j,
                    constraint_variables[1],
                    i
                )
                constraint = Constraint(
                    name=constraint_expression,
                    variables=constraint_variables,
                    expression=constraint_expression
                )
                constraints[constraint_expression] = constraint

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
        possible_combinations = set()
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
                possible_combinations.add(tuple(values))
        return possible_combinations

    @staticmethod
    def get_values(domain):
        if len(domain) == 1:
            for values in domain:
                return values
        return None
