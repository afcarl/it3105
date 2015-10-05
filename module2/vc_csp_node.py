from csp_node import CspNode
from copy import deepcopy


class VcCspNode(CspNode):
    def generate_children(self):
        """
        The general generate_children of CspNode works, but this slightly modified version
        seems to perform better
        :return:
        """
        children = set()
        if self.is_dead_end():
            return children

        for domain_name, domain in self.domains.iteritems():
            if len(domain) == 1:
                neighbour_names = self.CONSTRAINT_NETWORK.get_neighbour_names(domain_name)
                sorted_neighbour_names = sorted(
                    neighbour_names,
                    key=lambda name: len(self.domains[name])
                )

                for neighbour_name in sorted_neighbour_names:
                    if len(self.domains[neighbour_name]) > 1:
                        for value in self.domains[neighbour_name]:
                            domains_copy = deepcopy(self.domains)
                            domains_copy[neighbour_name] = {value}
                            child = self.__class__(domains_copy)
                            child.rerun(neighbour_name)
                            children.add(child)
                        return children  # Only assume a value for ONE undecided domain
        return children

    def get_num_uncolored_vertices(self):
        num_uncolored_vertices = 0
        for domain in self.domains.itervalues():
            if self.CONSTRAINT_NETWORK.get_color_id(domain) == -1:
                num_uncolored_vertices += 1
        return num_uncolored_vertices
