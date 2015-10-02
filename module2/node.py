#from module1.node import Node
import itertools
from collections import deque


class TodoRevise:
    def __init__(self, focal_variable, constraint):
        self.focal_variable = focal_variable
        self.constraint = constraint

    def __repr__(self):
        return "focal variable: " + str(self.focal_variable)\
               + ", constraint: " + self.constraint.expression


class CspNode:#(Node):
    """
    domains: dict
    constraints: list of constraints
    """
    def __init__(self, domains, constraints):
        self.domains = domains
        self.constraints = constraints
        self.queue = deque()  # todo: improve data structure

    def initialize_csp(self):
        for constraint in self.constraints.itervalues():
            for variable in constraint.variables:
                self.queue.append(TodoRevise(focal_variable=variable, constraint=constraint))

    def domain_filtering(self):
        while self.queue:
            todo_revise = self.queue.popleft()
            print 'processing agenda item', todo_revise
            domain_was_reduced = self.revise(todo_revise.focal_variable, todo_revise.constraint)
            if domain_was_reduced:
                # TODO: find affected pairs, and push them
                #self.queue.append(new_todo_revise)
                print 'domain was reduced'
                pass

    def has_possible_combinations(self, focal_variable, value, constraint):
        domains_as_list_of_lists = []
        for variable in constraint.ordered_variables:
            if variable == focal_variable:
                domains_as_list_of_lists.append([value])
            else:
                domains_as_list_of_lists.append(self.domains[variable])
        combinations = list(itertools.product(*domains_as_list_of_lists))
        for combination in combinations:
            if constraint.is_satisfied(*combination):
                return True
        return False

    def revise(self, focal_variable, constraint):
        values_to_remove = set()
        has_reduced_domain = False
        print 'revising, and this is self.domains', self.domains
        print 'focal_variable', focal_variable
        for value in self.domains[focal_variable]:
            # find all combinations of the other variables, given their current domain
            has_possible_combinations = self.has_possible_combinations(
                focal_variable=focal_variable,
                value=value,
                constraint=constraint
            )
            if not has_possible_combinations:
                values_to_remove.add(value)
                has_reduced_domain = True

        # remove all values in values_to_remove from the domain
        self.domains[focal_variable] -= values_to_remove

        return has_reduced_domain
