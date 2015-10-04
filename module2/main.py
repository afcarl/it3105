from gfx import Gfx
import argparse
from node import CspNode
from constraint_network import VertexColorVariable, VertexColorConstraintNetwork
from module1.a_star import AStar
from copy import deepcopy


class Main(object):
    def __init__(self):
        num_colors = 4  # TODO

        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '-i',
            '--input',
            dest='filename',
            type=str,
            help='The name of the input file',
            required=True
        )
        args = arg_parser.parse_args()

        f = open(args.filename)
        lines = []
        for line in f:
            lines.append(line.strip())
        f.close()

        num_vertices, num_edges, vertices, edges = self.parse_lines(lines)

        # initialize constraint network

        initial_domain = range(num_colors)
        self.constraint_network = VertexColorConstraintNetwork(
            vertices=vertices,
            edges=edges,
            initial_domain=initial_domain
        )

        self.gfx = Gfx()
        self.a_star = AStar(draw=self.gfx.draw)

        self.run()

    @staticmethod
    def insert_variable_prefix(i):
        return "v" + str(i)

    @staticmethod
    def parse_lines(lines):
        """
        Parse the lines of the input file according to the spec
        :param lines: array
        """
        num_vertices, num_edges = map(int, lines[0].split(' '))

        vertices = []
        for i in range(1, num_vertices + 1):
            i, x, y = lines[i].split(' ')
            i = Main.insert_variable_prefix(i)
            x, y = float(x), float(y)
            vertex = VertexColorVariable(i=i, x=x, y=y)
            vertices.append(vertex)

        edges = []
        for i in range(num_vertices + 1, num_vertices + 1 + num_edges):
            i1, i2 = map(Main.insert_variable_prefix, lines[i].split(' '))
            edges.append((i1, i2))

        return num_vertices, num_edges, vertices, edges

    def run(self):
        # TODO

        start_node = CspNode(
            domains=deepcopy(self.constraint_network.domains),
            constraints=self.constraint_network.constraints,
            constraint_network=self.constraint_network,
            g=0
        )
        start_node.initialize_csp()
        start_node.domain_filtering()

        print 'running'
        self.a_star.run(start_node=start_node)

if __name__ == '__main__':
    Main()
