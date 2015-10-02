#from module1.node import Node


class TodoRevise:
    def __init__(self, focal_variable):
        self.focal_variable = focal_variable


class CspNode:#(Node):
    def __init__(self, domains, constraints):
        self.domains = domains
        self.constraints = constraints
        self.queue = []  # todo: improve data structure

    def initialize_csp(self):
        for constraint in self.constraints:
            for variable in constraint:
                self.queue.append(TodoRevise(focal_variable=variable))

    def has_possible_combinations(self, focal_variable, value, constraint):


        return False

    def revise(self, focal_variable, constraint):
        values_to_remove = set()
        has_reduced_domain = False
        for value in self.domains(focal_variable):
            # find all combinations of the other variables, given their domain
            has_possible_combinations = self.has_possible_combinations(
                focal_variable=focal_variable,
                value=value,
                constraint=constraint
            )
            if not has_possible_combinations:
                values_to_remove.add(value)
                has_reduced_domain = True
        return has_reduced_domain
