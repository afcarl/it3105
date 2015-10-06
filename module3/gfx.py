import sys, pygame

pygame.display.init()


class Gfx(object):
    """
    This class takes care of drawing the state of the search to a window using pygame
    """
    size = width, height = 960, 540
    WHITE = 255, 255, 255
    GREY = 128, 128, 128

    def __init__(self, grid_width, grid_height, fps):
        self.grid_width = grid_width
        self.grid_height = grid_height

        self.GU_X = self.width / float(grid_width)
        self.GU_Y = self.height / float(grid_height)

        self.screen = pygame.display.set_mode(self.size)

        self.clock = pygame.time.Clock()  # used for limiting the fps, so one can see each step
        self.fps = fps

    def draw_tile(self, x, y, color):
        rect = pygame.Rect(
            x * self.GU_X + 1,
            y * self.GU_Y + 1,
            self.GU_X - 2,
            self.GU_Y - 2
        )
        pygame.draw.rect(self.screen, color, rect)

    def draw_rows(self, node):
        for variable_name, domain in node.domains.iteritems():
            if variable_name[0] == 'r':
                values = node.CONSTRAINT_NETWORK.get_values(domain)
                if values is not None:
                    i = int(variable_name[1:])
                    for j in xrange(len(values)):
                        column_value = values[j]
                        color = self.GREY if column_value == 1 else self.WHITE
                        self.draw_tile(j, i, color)

    def draw(self, current_node, ancestors, closed_list, open_list):
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

        self.draw_rows(current_node)

        pygame.display.flip()
