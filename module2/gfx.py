import sys, pygame

pygame.init()

# TODO: make sure the csp can handle up to 8 colors


class Gfx(object):
    """
    This class takes care of drawing the state of the search to a window using pygame
    """
    size = width, height = 960, 540
    WHITE = 255, 255, 255
    BLACK = 0, 0, 0
    YELLOW = 255, 236, 193
    GREEN = 47, 160, 19
    GREY = 128, 128, 128
    BLUE = 109, 142, 224
    PINK = 255, 130, 234

    def __init__(self, fps):
        self.GU_X = self.width / 16
        self.GU_Y = self.height / 9

        self.screen = pygame.display.set_mode(self.size)

        self.clock = pygame.time.Clock()  # used for limiting the fps, so one can see each step
        self.fps = fps

    def draw_dots(self, nodes):
        for node in nodes:
            pygame.draw.circle(self.screen, node.get_color(), [60, 250], 40)

    def draw_arcs(self, arcs):
        for arc in arcs:
            pass  # TODO: draw arcs

    def draw(self, current_node):
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

        self.draw_dots(current_node.get_dots())
        self.draw_arcs(current_node.get_arcs())

        pygame.display.flip()
