from csp_node import CspNode


class VcCspNode(CspNode):
    def __init__(self, domains, g=None, h=None, parent=None):
        """
        domains: dict
        """
        super(VcCspNode, self).__init__(domains=domains, g=g, h=h, parent=parent)
        self.hash_cache = None

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
