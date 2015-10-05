import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from module2.csp_node import CspNode
from copy import deepcopy


class NgCspNode(CspNode):
    def __init__(self, domains, g=None, h=None, parent=None):
        """
        domains: dict
        """
        super(NgCspNode, self).__init__(domains=domains, g=g, h=h, parent=parent)
        self.hash_cache = None  # TODO: check if this is used

    def __eq__(self, other_node):
        # TODO: check if this works
        # TODO: consider moving this to CspNode
        for domain_name, domain in self.domains.iteritems():
            other_domain = other_node.domains[domain_name]
            if domain != other_domain:
                return False
        return True

    def __hash__(self):
        # TODO: check if this works
        # TODO: consider moving this to CspNode
        if self.hash_cache is not None:
            return self.hash_cache
        frozen_items = [frozenset(domain) for domain in self.domains.itervalues()]
        hash_result = hash(tuple(sorted(frozen_items)))
        self.hash_cache = hash_result
        return hash_result

    def is_solution(self):
        # TODO: check if this works
        # TODO: consider moving this to CspNode
        for domain in self.domains.itervalues():
            if len(domain) != 1:
                return False
        return True

    def calculate_h(self):
        # TODO: check if this works
        # TODO: consider moving this to CspNode
        domain_size_sum = 0

        for domain in self.domains.itervalues():
            domain_len = len(domain)
            if domain_len == 0:
                self.h = 99999999999999999 * self.H_MULTIPLIER
                return
            domain_size_sum += domain_len

        self.h = domain_size_sum * self.H_MULTIPLIER  # rough estimate, but not admissible

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

