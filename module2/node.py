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
    """
    domains: dict
    constraints: list of constraints
    constraint_network: ConstraintNetwork instance
    """

    def __init__(self, domains, constraints, constraint_network, g=None, h=None, parent=None):
        self.domains = domains
        self.constraints = constraints
        self.queue = deque()
        self.constraint_network = constraint_network  # TODO: this should be static
        super(CspNode, self).__init__(g=g, h=h, parent=parent)

    def initialize_csp(self):
        for constraint in self.constraints.itervalues():
            for variable in constraint.variables:
                self.queue.append(TodoRevise(focal_variable=variable, constraint=constraint))

    def domain_filtering(self):
        while self.queue:
            todo_revise = self.queue.popleft()
            # print 'processing agenda item', todo_revise
            domain_was_reduced = self.revise(todo_revise.focal_variable, todo_revise.constraint)
            if domain_was_reduced:
                todo_constraints = self.constraint_network.get_constraints_by_variable(
                    variable=todo_revise.focal_variable,
                    current_constraint=todo_revise.constraint
                )
                for constraint in todo_constraints:
                    for variable in constraint.variables:
                        # if variable == todo_revise.focal_variable:
                        #    continue  # TODO: not sure if I should include this
                        self.queue.append(
                            TodoRevise(
                                focal_variable=variable,
                                constraint=constraint
                            )
                        )

                # print 'domain was reduced'
            else:
                pass
                # print 'domain was not reduced'
        # print 'domain filtering is done!'

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
        # print 'revising, and this is self.domains', self.domains
        # print 'focal_variable', focal_variable
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

    def rerun(self, assumed_variable):  # TODO: actually use this function
        todo_constraints = self.constraint_network.get_constraints_by_variable(
            variable=assumed_variable
        )
        for constraint in todo_constraints:
            for variable in constraint.variables:
                # if variable == todo_revise.focal_variable:
                #    continue  # TODO: not sure if I should include this
                self.queue.append(
                    TodoRevise(
                        focal_variable=variable,
                        constraint=constraint
                    )
                )

    def calculate_h(self):
        self.h = 1  # TODO: implement

    def generate_children(self):
        return []  # TODO: implement

    def is_solution(self):
        for domain in self.domains.itervalues():
            if len(domain) != 1:
                return False
        return True  # TODO: test

    def __eq__(self, other_node):
        for domain_name, domain in self.domains.iteritems():
            other_domain = other_node.domains[domain_name]
            if domain != other_domain:
                return False
        return True  # TODO: test

    def __hash__(self):
        #if self.hash_cache:
        #    return self.hash_cache  # TODO: check if uncommenting this (and that below) improves perf
        frozen_items = [frozenset(domain) for domain in self.domains.itervalues()]
        hash_result = hash(tuple(sorted(frozen_items)))
        # self.hash_cache = hash_result
        return hash_result
