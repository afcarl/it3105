import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from module1.base_node import BaseNode
import itertools
from collections import deque


class TodoRevise:
    def __init__(self, focal_variable, constraint):
        self.focal_variable = focal_variable
        self.constraint = constraint

    def __repr__(self):
        return "focal variable: " + str(self.focal_variable) \
               + ", constraint: " + self.constraint.expression


class CspNode(BaseNode):
    H_MULTIPLIER = 1
    CONSTRAINT_NETWORK = None
    CONSTRAINTS = None

    def __init__(self, domains, g=None, h=None, parent=None):
        """
        domains: dict
        """
        self.domains = domains
        self.queue = deque()
        super(CspNode, self).__init__(g=g, h=h, parent=parent)

    @staticmethod
    def set_constraint_network(constraint_network):
        CspNode.CONSTRAINT_NETWORK = constraint_network

    @staticmethod
    def set_constraints(constraints):
        CspNode.CONSTRAINTS = constraints

    def initialize_csp(self):
        for constraint in self.CONSTRAINTS.itervalues():
            for variable in constraint.variables:
                self.queue.append(TodoRevise(focal_variable=variable, constraint=constraint))

    def domain_filtering(self):
        while self.queue:
            todo_revise = self.queue.popleft()
            domain_was_reduced = self.revise(todo_revise.focal_variable, todo_revise.constraint)
            if domain_was_reduced:
                todo_constraints = self.CONSTRAINT_NETWORK.get_constraints_by_variable(
                    variable=todo_revise.focal_variable,
                    current_constraint=todo_revise.constraint
                )
                for constraint in todo_constraints:
                    for variable in constraint.variables:
                        if variable == todo_revise.focal_variable:
                            continue  # optimization
                        self.queue.append(
                            TodoRevise(
                                focal_variable=variable,
                                constraint=constraint
                            )
                        )

    def has_possible_combinations(self, focal_variable, value, constraint):
        domains_as_list_of_lists = [
            (value,) if variable == focal_variable else self.domains[variable]
            for variable in constraint.ordered_variables
        ]

        for combination in itertools.product(*domains_as_list_of_lists):
            if constraint.is_satisfied(*combination):
                return True
        return False

    def revise(self, focal_variable, constraint):
        values_to_remove = set()
        has_reduced_domain = False
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

    def rerun(self, assumed_variable):
        todo_constraints = self.CONSTRAINT_NETWORK.get_constraints_by_variable(
            variable=assumed_variable
        )
        for constraint in todo_constraints:
            for variable in constraint.variables:
                if variable == assumed_variable:
                    continue  # optimization
                self.queue.append(
                    TodoRevise(
                        focal_variable=variable,
                        constraint=constraint
                    )
                )
        self.domain_filtering()

    def is_dead_end(self):
        for domain in self.domains.itervalues():
            if len(domain) == 0:
                return True
        return False
