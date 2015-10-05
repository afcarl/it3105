import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from module1.base_node import BaseNode
import itertools
from collections import deque
from copy import deepcopy


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
        self.hash_cache = None
        super(CspNode, self).__init__(g=g, h=h, parent=parent)

    def __eq__(self, other_node):
        for domain_name, domain in self.domains.iteritems():
            other_domain = other_node.domains[domain_name]
            if domain != other_domain:
                return False
        return True

    def __hash__(self):
        if self.hash_cache is not None:
            return self.hash_cache
        frozen_items = [frozenset(domain) for domain in self.domains.itervalues()]
        hash_result = hash(tuple(sorted(frozen_items)))
        self.hash_cache = hash_result
        return hash_result

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

    def generate_children(self):
        children = set()
        if self.is_dead_end():
            return children

        domain_names_sorted_by_size = sorted(
            self.domains,
            key=lambda name: len(self.domains[name])
        )

        for domain_name in domain_names_sorted_by_size:
            if len(self.domains[domain_name]) > 1:
                for value in self.domains[domain_name]:
                    domains_copy = deepcopy(self.domains)
                    domains_copy[domain_name] = {value}
                    child = self.__class__(domains_copy)
                    child.rerun(domain_name)
                    children.add(child)
                return children  # Only assume a value for ONE undecided domain
        return children

    def is_solution(self):
        for domain in self.domains.itervalues():
            if len(domain) != 1:
                return False
        return True

    def calculate_h(self):
        domain_size_sum = 0

        for domain in self.domains.itervalues():
            domain_len = len(domain)
            if domain_len == 0:
                self.h = 99999999999999999 * self.H_MULTIPLIER
                return
            domain_size_sum += domain_len

        self.h = domain_size_sum * self.H_MULTIPLIER  # rough estimate, but not admissible

    def get_num_unsatisfied_constraints(self):
        return self.CONSTRAINT_NETWORK.get_num_unsatisfied_constraints(domains=self.domains)
