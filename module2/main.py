from gfx import Gfx
import argparse
from node import Vertex


class Main(object):
    def __init__(self):
        num_colors = 8  # TODO



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
        # generate positions
        # generate arcs between dots

        # parse lines

        self.run()

    @staticmethod
    def parse_lines(lines):
        """
        Parse the lines of the input file according to the spec
        :param lines: array
        """
        num_vertices, num_edges = map(int, lines[0].split(' '))
        print num_vertices, num_edges

        vertices = []
        for i in range(1, num_vertices + 1):
            i, x, y = lines[i].split(' ')
            i, x, y = int(i), float(x), float(y)
            vertex = Vertex(i=i, x=x, y=y)
            vertices.append(vertex)
            print i, x, y

        edges = []
        for i in range(num_vertices + 1, num_vertices + 1 + num_edges):
            i1, i2 = map(int, lines[i].split(' '))
            edges.append((i1, i1))
            print i1, i2

        return num_vertices, num_edges, vertices, edges

    def run(self):
        # TODO
        print 'running'
