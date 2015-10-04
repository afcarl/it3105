import sys, pygame

pygame.init()

# TODO: make sure the csp can handle up to 8 colors


class Gfx(object):
    """
    This class takes care of drawing the state of the search to a window using pygame
    """
    size = width, height = 960, 540

    VERTEX_SIZE = 8
    EDGE_WIDTH = 1

    COLOR_MAP = {
        -1: (128, 128, 128),  # grey
        0: (255, 236, 130),  # yellow
        1: (47, 160, 19),  # green
        2: (109, 142, 224),  # blue
        3: (255, 130, 234),  # pink
        4: (132, 19, 160),  # purple
        5: (224, 191, 109),  # bronze
        6: (89, 255, 208),  # teal
        7: (255, 79, 108)  # red
    }
    WHITE = 255, 255, 255
    BLACK = 0, 0, 0

    def __init__(self, fps=30.0):
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()  # used for limiting the fps, so one can see each step
        self.fps = fps

    def scale_position(self, x, y):
        """
        Takes in normalized x and y, i.e. with range [0, 1]
        :param x:
        :param y:
        :return: x and y scaled to the size of the window, with 5% margin
        """
        return int(round((0.05 + 0.9 * x) * self.width)), int(round((0.05 + 0.9 * y) * self.height))

    def draw_vertices(self, node):
        for domain_name, domain in node.domains.iteritems():
            x, y = node.CONSTRAINT_NETWORK.get_position(domain_name)
            x, y = self.scale_position(x, y)
            color_id = node.CONSTRAINT_NETWORK.get_color_id(domain)
            color = self.COLOR_MAP[color_id]
            pygame.draw.circle(self.screen, color, [x, y], self.VERTEX_SIZE)

    def draw_edges(self, node):
        for edge in node.CONSTRAINT_NETWORK.edges:
            vertex1, vertex2 = edge
            x1, y1 = node.CONSTRAINT_NETWORK.get_position(vertex1)
            x1, y1 = self.scale_position(x1, y1)
            x2, y2 = node.CONSTRAINT_NETWORK.get_position(vertex2)
            x2, y2 = self.scale_position(x2, y2)

            pygame.draw.line(self.screen, self.BLACK, [x1, y1], [x2, y2], self.EDGE_WIDTH)

    def draw(self, current_node, ancestors, open_list, closed_list):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.fps /= 2  # halve the fps
                if event.key == pygame.K_UP:
                    self.fps *= 2  # double the fps
                    if self.fps > 256.0:
                        self.fps = 256.0

        self.clock.tick(self.fps)

        self.screen.fill(self.WHITE)

        self.draw_edges(current_node)
        self.draw_vertices(current_node)

        pygame.display.flip()

