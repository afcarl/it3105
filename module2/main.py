import argparse
from vc_csp_node import VcCspNode
from vc_constraint_network import VertexColorVariable, VertexColorConstraintNetwork
from module1.a_star import AStar
from copy import deepcopy
import time


class Main(object):
    def __init__(self):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '-i',
            '--input',
            dest='filename',
            type=str,
            help='The name of the input file',
            required=True
        )
        arg_parser.add_argument(
            '--mode',
            dest='mode',
            type=str,
            choices=['astar', 'bfs', 'dfs'],
            required=False,
            default="astar"
        )
        arg_parser.add_argument(
            '-k',
            '--num-colors',
            dest='num_colors',
            type=int,
            choices=[2, 3, 4, 5, 6, 7, 8],
            required=True,
        )
        arg_parser.add_argument(
            '--fps',
            dest='fps',
            type=float,
            required=False,
            default=16.0
        )
        arg_parser.add_argument(
            '--draw-every',
            dest='draw_every',
            help='Use this argument to skip frames when visualizing large and complex problems',
            type=int,
            required=False,
            default=1
        )
        arg_parser.add_argument(
            '--disable-gfx',
            nargs='?',
            dest='disable_gfx',
            const=True,
            required=False,
            default=False
        )

        arg_parser.add_argument(
            '--print-execution-time',
            nargs='?',
            dest='print_execution_time',
            help='At the end of the run, print the execution time of the A* algorithm. Useful for'
                 ' testing the performance of the algorithm while gfx is disabled.',
            const=True,
            required=False,
            default=False
        )
        args = arg_parser.parse_args()

        if args.mode == 'bfs':
            VcCspNode.H_MULTIPLIER = 0
        elif args.mode == 'dfs':
            VcCspNode.H_MULTIPLIER = 0
            VcCspNode.ARC_COST_MULTIPLIER = 0

        f = open(args.filename)
        lines = []
        for line in f:
            lines.append(line.strip())
        f.close()

        num_vertices, num_edges, vertices, edges = self.parse_lines(lines)

        # initialize constraint network
        initial_domain = range(args.num_colors)
        self.constraint_network = VertexColorConstraintNetwork(
            vertices=vertices,
            edges=edges,
            initial_domain=initial_domain
        )

        if not args.disable_gfx:
            from gfx import Gfx
            self.gfx = Gfx(fps=args.fps)

        self.a_star = AStar(
            draw=self.gfx.draw if not args.disable_gfx else lambda _: 0,
            disable_gfx=args.disable_gfx,
            draw_every=args.draw_every,
            print_path=False
        )

        if args.print_execution_time:
            self.start_time = time.time()

        self.run()

        if args.print_execution_time:
            print "execution time: %s seconds" % (time.time() - self.start_time)

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
        VcCspNode.set_constraint_network(self.constraint_network)
        VcCspNode.set_constraints(self.constraint_network.constraints)
        start_node = VcCspNode(
            domains=deepcopy(self.constraint_network.domains),
            g=0
        )
        # a little optimization: pick a color for the first vertex
        first_domain = start_node.domains.itervalues().next()
        while len(first_domain) > 1:
            first_domain.pop()

        start_node.initialize_csp()
        start_node.domain_filtering()

        success, end_node = self.a_star.run(start_node=start_node)

        num_unsatisfied_constraints = end_node.get_num_unsatisfied_constraints()
        print 'number of unsatisfied constraints:', num_unsatisfied_constraints

        num_uncolored_vertices = end_node.get_num_uncolored_vertices()
        print 'number of uncolored vertices', num_uncolored_vertices

if __name__ == '__main__':
    Main()
