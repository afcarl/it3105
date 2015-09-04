import sys, pygame

pygame.init()


class Gfx(object):
    size = width, height = 960, 540
    WHITE = 255, 255, 255  # undiscovered tiles
    BLACK = 0, 0, 0  # closed tiles
    YELLOW = 255, 236, 193  # open tiles
    GREEN = 47, 160, 19  # goal
    GREY = 128, 128, 128  # barriers
    BLUE = 109, 142, 224  # start
    PINK = 255, 130, 234  # current node
    DARK_PINK = 178, 110, 149  # nodes backtracked from current node

    def __init__(self, board):
        self.board = board

        self.GU_X = self.width / float(board.rect.width)
        self.GU_Y = self.height / float(board.rect.height)

        self.screen = pygame.display.set_mode(self.size)

    def flip_vertically(self, y):
        """
        We need to use this because in the specification, (0, 0) is the lower left corner
        and not the upper left corner, which is the default when drawing stuff in pygame
        :param y:
        """
        return self.board.rect.height - 1 - y

    def draw_tile(self, x, y, color):
        rect = pygame.Rect(
            x * self.GU_X + 1,
            self.flip_vertically(y) * self.GU_Y + 1,
            self.GU_X - 2,
            self.GU_Y - 2
        )
        pygame.draw.rect(self.screen, color, rect)

    def draw_barriers(self):
        for tile in self.board.inaccessible_tiles:
            self.draw_tile(tile[0], tile[1], self.GREY)

    def draw_start(self):
        self.draw_tile(self.board.start.x, self.board.start.y, self.BLUE)

    def draw_goal(self):
        self.draw_tile(self.board.goal.x, self.board.goal.y, self.GREEN)

    def draw_current_node(self, node):
        self.draw_tile(node.x, node.y, self.PINK)

    def draw_ancestors(self, ancestors):
        for ancestor in ancestors:
            self.draw_tile(ancestor.x, ancestor.y, self.DARK_PINK)

    def draw(self, current_node):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        self.screen.fill(self.WHITE)

        self.draw_barriers()
        self.draw_goal()
        self.draw_current_node(current_node)
        self.draw_ancestors(current_node.get_ancestors())
        self.draw_start()

        # TODO: draw open list and closed list? dunno if necessary

        pygame.display.flip()
